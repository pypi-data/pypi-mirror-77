from ..handler import RequestHandler
from http import HTTPStatus
import os,mimetypes

def Property(func):
    '''Wrapper for static properties for `Modlues`'''
    @property
    def wrapper(self):
        return getattr(self,'_' + func.__name__)
    @wrapper.setter
    def wrapper(self,value):
        return setattr(self,'_' + func.__name__,value)
    return wrapper

class Utilties():
    @staticmethod
    def GuessMIME(path):
        '''Guesses a file's MIME type'''
        return mimetypes.MimeTypes().guess_type(path)[0]
class UnfinishedException(Exception):
    '''Exceptions that are non-fatal,and did't affect the response'''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
class HTTPModules():
    '''Modules that are designed for HTTP Adapters'''
    @staticmethod
    def Redirect(request:RequestHandler,target='',code=HTTPStatus.FOUND):
        '''Redirects to other URLs'''
        request.send_response(code)
        request.send_header('Location',target)
        request.end_headers()

    @staticmethod
    def RestrictVerbs(request:RequestHandler,verbs=['GET','POST']):
        '''Restricts HTTP Verbs,does nothing if the verb is in the `verbs` list'''
        if not request.command in verbs:
            raise UnfinishedException('Verb %s is not allowed' % request.command)
    
    @staticmethod
    def IndexFolder(request:RequestHandler,path,stylesheet='',encoding='utf-8'):
        '''Automaticly indexes the folder and renders a human readable HTML page'''
        if os.path.isfile(path):return HTTPModules.WriteStream(request,path)
        # Call `WriteStream` if we are somehow given a file path
        request.send_response(HTTPStatus.OK)
        request.send_header('Content-Type','text/html; charset=' + encoding)
        request.end_headers()
        html = f'''\
<head>
    <meta charset="UTF-8">
    <title>Index of {path}</title>
    <style>{stylesheet}</style>
</head>
<body>
    <h1>Index of {path}</h1>
    <hr><pre><a href="..">..</a>\n'''
        for item in sorted(os.listdir(path)):
            html += f'<a href="{item}/"/>{item}/</a>\n' if os.path.isdir(os.path.join(path,item)) else f'<a href="{item}"/>{item}</a>\n'
        html+= f'''</pre><hr><body>\n'''
        HTTPModules.WriteString(request,html)
        request.wfile.flush()

    @staticmethod
    def WriteString(request:RequestHandler,string):
        '''Appends a string (encoded here) or a bytesarray to the buffer'''
        return request.wfile.write(str(string).encode() if type(string) != bytes else string)

    @staticmethod
    def WriteStream(request:RequestHandler,stream,chunck=32768,support_range=True):
        '''Sends a file with path,or sends a ByteIO-like object.will flush the headers,and sends a valid HTTP response code
                
        `stream`  :   Either a `str` for filename or a `ByteIO` for streamed IOs

        `chunck`  :   Chunk size in bytes

        `support_range`:  Whether supports HTTP 206s or not
        '''
        if isinstance(stream,str):
            # Try to parse the `file` as a file path
            if not os.path.exists(stream):
                return request.send_error(404,explain=f'The reuqested file {stream} is not present on the target server')
            f,s = open(stream,'rb'),os.stat(stream).st_size
        else:
            if getattr(stream,'read'):
                f,s = stream,0
            else:raise IOError('File cannot be read')
        # Always add this header first
        # For sending all of the file in chunks
        def send_once():                        
            request.send_response(HTTPStatus.OK)
            if s:# a `real` file,which has file size properites
                if support_range:request.send_header('Accept-Ranges','bytes')
                request.send_header('Content-Length',str(s))
                request.send_header('Content-Type',Utilties.GuessMIME(stream))
            request.end_headers()            
            chunk = f.read(chunck)
            while chunk:
                try:
                    request.wfile.write(chunk)
                    chunk = f.read(chunck)
                except Exception:
                    # Connection closed while transmitting,or something else
                    return True
            f.close()
            return True
        # For HTTP 206 : Range headers
        def send_range():
            # Checks range header (if it exists and is satisfiable)
            if not request.headers.get('Range'):return False
            # If not exist,let `send_once` handle it. Parse range header if exsists
            Range = request.headers.get('Range')
            if not Range[:6] == 'bytes=' : return False
            # Does not start with `bytes`,let `send_once` do it afterwards
            Range = Range[6:]
            start,end = Range.split('-')
            start,end = int(start if start else 0),int(end if end else s)
            if not (start >= 0 and start < s and end > 0 and end > start and end <= s):
                # Range not satisfiable
                request.send_response(HTTPStatus.REQUESTED_RANGE_NOT_SATISFIABLE)
                request.end_headers()
                # Stop the routine right here
                return True
            # Otherwise,good to go!
            request.send_response(HTTPStatus.PARTIAL_CONTENT)
            request.send_header('Accept-Ranges','bytes')
            request.send_header('Content-Length',str(end - start))
            request.send_header('Content-Type',Utilties.GuessMIME(stream))
            request.send_header('Content-Range','bytes %s-%s/%s' % (start,end,s))
            request.end_headers()            
            try:
                read = start
                # How much have we already read?
                f.seek(start)
                # Seek from the start
                for current in range(start,end,chunck):
                    if (current - read) > 0:request.wfile.write(f.read(current - read))
                    # Read & send the delta amount of data
                    read = current
                request.wfile.write(f.read(end - current))
                # Finally,send the rest
            except Exception:
                return True
            return True
        if support_range and s:
            # Range header is supported and the file is a REAL file
            if send_range():return True
        # Otherwise
        return send_once()

def PathMaker(maker):
    def wrapper(target):
        func = maker(target)
        func.__setattr__('maker',maker)
        func.__setattr__('target',target)
        return func
    return staticmethod(wrapper)

class PathMakerModules():
    '''
    Provides static methods for `PathMaker` to map paths

    The methods,takes 1 string argument and returns a `callable`,
    which again,takes 1 string argument then returns a bool value

    The methods are annotated.Two more attributes are added to the returned funtion:

        `maker`     :       The original PathMakerModule('s Module)
        `target`    :       The Pathmaker target
    '''
    @staticmethod
    def GetModuleProperty(module):
        return {'maker':module.__getattribute__('maker'),'target':module.__getattribute__('target')}

    @PathMaker
    def Absolute(target):
        '''Checks if the path is exact to the target'''
        return lambda path:path == target

    @PathMaker
    def AbsoluteWithoutCaps(target):
        '''Checks if the path is exact to the target without matching captial letters'''
        return lambda path:path.lower() == target.lower()
    
    @PathMaker
    def DirectoryPath(target):
        '''Checks if the path has the targeted base path,which is useful for non-absolute paths
        e.g.:

            target
                /static/js/
            path
                /static/js               
                /static/js/
                /static/js/core.js
            This WILL work!
        '''
        if target[-1] != '/':raise Exception('Directory path-making must end with backslash (/) !')
        def check(path):
            if path[:len(target)] == target:
                # the url begins with the target path with the backslash
                return True            
            return PathMakerModules.Absolute(target[:-1])(path)
            # Otherwise,if the path is exactly the same as the target
            # without backslash,still returns True.Otherwise False
        return check