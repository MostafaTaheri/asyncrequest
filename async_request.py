import aiohttp
import asyncio

from typing import Optional


class Request(object):
    """This class implements the async Requests API.

    Example:
        >>> req = request(method='GET', url='https://httpbin.org/get')

    Returns:
        A list of json.
    """
    def __init__(self):
        self.header = {
            aiohttp.hdrs.CONNECTION: aiohttp.hdrs.KEEP_ALIVE,
            'Authorization': "bear your token"
        }
        self.request_timeout = aiohttp.ClientTimeout(total=2 * 60)
        self.session_timeout = self.request_timeout

    @property
    def _time_out(self):
        """Returns timeout value."""
        return self.request_timeout

    @_time_out.setter
    def _time_out(self, value):
        """Set a new value for timeout."""
        self.request_timeout = aiohttp.ClientTimeout(total=value)

    @property
    def _client_session(self):
        """Client session is the recommended interface for making HTTP requests.

        Session encapsulates a connection pool (connector instance) and supports
            keepalives by default. Unless you are connecting to a large, unknown
            number of different servers over the lifetime of your application, it
            is suggested you use a single session for the lifetime of your application
            to benefit from connection pooling.
            The client session supports the context manager protocol for self closing.

        Arguments:
            timeout: Timeout settings are stored in ClientTimeout data structure.
                By default aiohttp uses a total 5min timeout.
            connector: To limit amount of simultaneously opened connections
                you can pass limit parameter to connector.
        """
        timeout = self._time_out
        connector = aiohttp.TCPConnector(limit=30, loop=None)
        return aiohttp.ClientSession(connector=connector, timeout=timeout)

    def request(self, *, method: str, url: str, **kwargs: dict) -> dict:
        """Constructs and sends a :class:`Request <Request>`.

        Attributes:
            method: method for the new :class:`Request` object.
            url: URL for the new :class:`Request` object.
            params: (optional) Dictionary, list of tuples or bytes to send
                in the query string for the :class:`Request`.
            data: (optional) Dictionary, list of tuples, bytes, or file-like
                object to send in the body of the :class:`Request`.
            json: (optional) A JSON serializable Python object to send in the body of the :class:`Request`.
            headers: (optional) Dictionary of HTTP Headers to send with the :class:`Request`.
            cookies: (optional) Dict or CookieJar object to send with the :class:`Request`.
            files: (optional) Dictionary of ``'name': file-like-objects`` (or ``{'name': file-tuple}``) for multipart encoding upload.
                ``file-tuple`` can be a 2-tuple ``('filename', fileobj)``, 3-tuple ``('filename', fileobj, 'content_type')``
                or a 4-tuple ``('filename', fileobj, 'content_type', custom_headers)``, where ``'content-type'`` is a string
                defining the content type of the given file and ``custom_headers`` a dict-like object containing additional headers
                to add for the file.
            auth: (optional) Auth tuple to enable Basic/Digest/Custom HTTP Auth.
            timeout: (optional) How many seconds to wait for the server to send data
                before giving up, as a float, or a :ref:`(connect timeout, read
                timeout) <timeouts>` tuple.
            timeout: float or tuple.
            allow_redirects: (optional) Boolean. Enable/disable GET/OPTIONS/POST/PUT/PATCH/DELETE/HEAD redirection. Defaults to ``True``.
            allow_redirects: bool.
            proxies: (optional) Dictionary mapping protocol to the URL of the proxy.
            verify: (optional) Either a boolean, in which case it controls whether we verify
                the server's TLS certificate, or a string, in which case it must be a path
                to a CA bundle to use. Defaults to ``True``.
            stream: (optional) if ``False``, the response content will be immediately downloaded.
            cert: (optional) if String, path to ssl client cert file (.pem). If Tuple, ('cert', 'key') pair.

        Returns:
            A dictionary of response.
        """
        return asyncio.run(self._request(method, url, **kwargs))

    async def _request(self,
                       method: str,
                       url: str,
                       params: Optional[str] = None,
                       data: Optional[str] = None,
                       json: Optional[str] = None,
                       **kwargs: dict) -> dict:
        """Constructs and sends a :class:`Request <Request>`.

        Attributes:
            method: method for the new :class:`Request` object.
            url: URL for the new :class:`Request` object.
            params: (optional) Dictionary, list of tuples or bytes to send
                in the query string for the :class:`Request`.
            data: (optional) Dictionary, list of tuples, bytes, or file-like
                object to send in the body of the :class:`Request`.
            json: (optional) A JSON serializable Python object to send in the body of the :class:`Request`.
            headers: (optional) Dictionary of HTTP Headers to send with the :class:`Request`.
            cookies: (optional) Dict or CookieJar object to send with the :class:`Request`.
            files: (optional) Dictionary of ``'name': file-like-objects`` (or ``{'name': file-tuple}``) for multipart encoding upload.
                ``file-tuple`` can be a 2-tuple ``('filename', fileobj)``, 3-tuple ``('filename', fileobj, 'content_type')``
                or a 4-tuple ``('filename', fileobj, 'content_type', custom_headers)``, where ``'content-type'`` is a string
                defining the content type of the given file and ``custom_headers`` a dict-like object containing additional headers
                to add for the file.
            auth: (optional) Auth tuple to enable Basic/Digest/Custom HTTP Auth.
            timeout: (optional) How many seconds to wait for the server to send data
                before giving up, as a float, or a :ref:`(connect timeout, read
                timeout) <timeouts>` tuple.
            timeout: float or tuple.
            allow_redirects: (optional) Boolean. Enable/disable GET/OPTIONS/POST/PUT/PATCH/DELETE/HEAD redirection. Defaults to ``True``.
            allow_redirects: bool.
            proxies: (optional) Dictionary mapping protocol to the URL of the proxy.
            verify: (optional) Either a boolean, in which case it controls whether we verify
                the server's TLS certificate, or a string, in which case it must be a path
                to a CA bundle to use. Defaults to ``True``.
            stream: (optional) if ``False``, the response content will be immediately downloaded.
            cert: (optional) if String, path to ssl client cert file (.pem). If Tuple, ('cert', 'key') pair.

        Returns:
            A dictionary of response.
        """
        return await asyncio.gather({
            'get':
            self._get(session=self._client_session,
                      url=url,
                      params=params,
                      headers=self.header,
                      timeout=self._time_out,
                      **kwargs),
            'post':
            self._post(session=self._client_session,
                       url=url,
                       data=data,
                       json=json,
                       headers=self.header,
                       timeout=self._time_out,
                       **kwargs),
            'put':
            self._put(session=self._client_session,
                      url=url,
                      data=data,
                      headers=self.header,
                      timeout=self._time_out,
                      **kwargs),
            'patch':
            self._patch(session=self._client_session,
                        url=url,
                        data=data,
                        headers=self.header,
                        timeout=self._time_out,
                        **kwargs),
            'delete':
            self._delete(session=self._client_session,
                         url=url,
                         headers=self.header,
                         timeout=self._time_out,
                         **kwargs)
        }.get(method.lower()))

    @staticmethod
    async def _get(session: aiohttp.ClientSession,
                   url: str,
                   timeout: aiohttp.ClientTimeout,
                   params: Optional[str] = None,
                   headers: Optional[dict] = None,
                   **kwargs: dict) -> dict:
        """Sends a get request.

        Attributes:
            session: It is the recommended interface for making HTTP requests.
            url: URL for the new :class:`Request` object.
            params: (optional) Dictionary, list of tuples or bytes to send
                in the query string for the :class:`Request`.
            headers: (optional) Dictionary of HTTP Headers to send with the :class:`Request`.
            \*\*kwargs: Optional arguments that ``request`` takes.

        Returns:
            A dictionary of response.
        """
        async with session.get(url=url,
                               params=params,
                               headers=headers,
                               timeout=timeout,
                               **kwargs) as response:
            response = await response.json()
        await session.close()
        return response

    @staticmethod
    async def _post(session: aiohttp.ClientSession,
                    url: str,
                    timeout: aiohttp.ClientTimeout,
                    data: Optional[str] = None,
                    json: Optional[str] = None,
                    headers: Optional[dict] = None,
                    **kwargs: dict) -> dict:
        """Sends a post request.

        Attributes:
            session: It is the recommended interface for making HTTP requests.
            url: URL for the new :class:`Request` object.
            data: (optional) Dictionary, list of tuples, bytes, or file-like
                object to send in the body of the :class:`Request`.
            json: (optional) json data to send in the body of the :class:`Request`.
            headers: (optional) Dictionary of HTTP Headers to send with the :class:`Request`.
            \*\*kwargs: Optional arguments that ``request`` takes.

        Returns:
             A dictionary of response.
        """
        async with session.post(url=url,
                                data=data,
                                json=json,
                                headers=headers,
                                timeout=timeout,
                                **kwargs) as response:
            response = await response.json()
        await session.close()
        return response

    @staticmethod
    async def _put(session: aiohttp.ClientSession,
                   url: str,
                   timeout: aiohttp.ClientTimeout,
                   data: Optional[str] = None,
                   headers: Optional[dict] = None,
                   **kwargs: dict) -> dict:
        """Sends a put request.

        Attributes:
            session: It is the recommended interface for making HTTP requests.
            url: URL for the new :class:`Request` object.
            data: (optional) Dictionary, list of tuples, bytes, or file-like
                object to send in the body of the :class:`Request`.
            headers: (optional) Dictionary of HTTP Headers to send with the :class:`Request`.
            \*\*kwargs: Optional arguments that ``request`` takes.

        Returns:
            A dictionary of response.
        """
        async with session.put(url=url,
                               data=data,
                               headers=headers,
                               timeout=timeout,
                               **kwargs) as response:
            response = await response.json()
        await session.close()
        return response

    @staticmethod
    async def _patch(session: aiohttp.ClientSession,
                     url: str,
                     timeout: aiohttp.ClientTimeout,
                     data: Optional[str] = None,
                     headers: Optional[dict] = None,
                     **kwargs: dict) -> dict:
        """Sends a patch request.

        Attributes:
            session: It is the recommended interface for making HTTP requests.
            url: URL for the new :class:`Request` object.
            data: (optional) Dictionary, list of tuples, bytes, or file-like
                object to send in the body of the :class:`Request`.
            headers: (optional) Dictionary of HTTP Headers to send with the :class:`Request`.
            \*\*kwargs: Optional arguments that ``request`` takes.

        Returns:
            A dictionary of response.
        """
        async with session.patch(url=url,
                                 data=data,
                                 headers=headers,
                                 timeout=timeout,
                                 **kwargs) as response:
            response = await response.json()
        await session.close()
        return response

    @staticmethod
    async def _delete(session: aiohttp.ClientSession,
                      url: str,
                      timeout: aiohttp.ClientTimeout,
                      headers: Optional[dict] = None,
                      **kwargs: dict) -> int:
        """Sends a delete request.

        Attributes:
            session: It is the recommended interface for making HTTP requests.
            url: URL for the new :class:`Request` object.
            headers: (optional) Dictionary of HTTP Headers to send with the :class:`Request`.
            \*\*kwargs: Optional arguments that ``request`` takes.

        Returns:
            A status code.
        """
        async with session.delete(url=url,
                                  headers=headers,
                                  timeout=timeout,
                                  **kwargs) as response:
            response = await response.status
        await session.close()
        return response
