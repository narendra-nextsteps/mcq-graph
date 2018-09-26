"""Connection creator."""
import json as _json
import random as _random
import requests as _requests

from . import settings as _db_settings


class TokenGenrator(object):

    def __init__(self, username, password, connection_urls):
        """Init the credentials for getting the auth token.

        Parameters
        ----------
        username : string
            username that exists in db.
        password : string
            password for the given user.
        connection_urls : list(string)
            list of connection strings for the db instances.

        """
        self.username = username
        self.password = password
        self.connection_urls = connection_urls
        self._auth_token = None

    def get_connection_indicies(self, pick_random_server):
        """Return the connection indicies."""
        connection_indices = list(range(len(self.connection_urls)))
        if not pick_random_server:
            return connection_indices
        _random.shuffle(connection_indices)
        return connection_indices

    def get_auth_token(self, pick_random_server=False):
        """Get auth token from given list of servers.

        pick_random_server : bool, optional
            pick selection of server by random
            (the default is False, which means select in the given order.)

        Returns
        -------
        string
            auth token generated from the server.

        """
        if self._auth_token is not None:
            return self._auth_token

        kwargs = {
            'data': '{"username":"%s","password":"%s"}' % (
                self.username, self.password
            )
        }

        for connection_index in self.get_connection_indicies(
                pick_random_server
        ):
            response = _requests.post(
                '%s/_open/auth' % self.connection_urls[connection_index],
                **kwargs
            )
            if response.ok:
                json_data = response.content
                if json_data:
                    data_dict = _json.loads(json_data)
                    self._auth_token = data_dict.get('jwt')
        return self._auth_token


class JWTAuth(_requests.auth.AuthBase):
    def __init__(self, token):
        self.token = token

    def __call__(self, r):
        # Implement JWT authentication
        r.headers['Authorization'] = 'Bearer %s' % self.token
        return r


def get_connection(
        username, password, connection_urls, is_gevent=False,
        pick_random_server=False
):
    """Get the connection for the given credentials.

    Parameters
    ----------
    username : string
        username that exists in db.
    password : string
        password for the given user.
    connection_urls : list(string)
        list of connection strings for the db instances.
    is_gevent : bool, optional
        mokey patchs to AikidoSession (the default is False,
        which means don't patch)
    pick_random_server : bool, optional
        pick selection of server by random
        (the default is False, which means select in the given order.)

    Returns
    -------
    pyArango.connection.Connection
        returns patched version if the connection is for gevent.

    """
    import pyArango.connection
    if is_gevent:
        import grequests

        class AikidoSession(object):
            def __init__(self, session_username, session_password):
                if session_username:
                    self.auth = JWTAuth(session_password)
                else:
                    self.auth = None

            def post(self, url, data=None, json=None, **kwargs):
                if data is not None:
                    kwargs['data'] = data
                if json is not None:
                    kwargs['json'] = json

                kwargs['auth'] = self.auth
                return grequests.map([grequests.post(url, **kwargs)])[0]

            def get(self, url, **kwargs):
                kwargs['auth'] = self.auth
                result = grequests.map([grequests.get(url, **kwargs)])[0]
                return result

            def put(self, url, data=None, **kwargs):
                if data is not None:
                    kwargs['data'] = data
                kwargs['auth'] = self.auth
                return grequests.map([grequests.put(url, **kwargs)])[0]

            def head(self, url, **kwargs):
                kwargs['auth'] = self.auth
                return grequests.map([grequests.put(url, **kwargs)])[0]

            def options(self, url, **kwargs):
                kwargs['auth'] = self.auth
                return grequests.map([grequests.options(url, **kwargs)])[0]

            def patch(self, url, data=None, **kwargs):
                if data is not None:
                    kwargs['data'] = data
                kwargs['auth'] = self.auth
                return grequests.map([grequests.patch(url, **kwargs)])[0]

            def delete(self, url, **kwargs):
                kwargs['auth'] = self.auth
                return grequests.map([grequests.delete(url, **kwargs)])[0]

            def disconnect(self):
                pass

        pyArango.connection.AikidoSession = AikidoSession
        auth_token = TokenGenrator(username, password, connection_urls)
        return pyArango.connection.Connection(
            username=username,
            password=auth_token.get_auth_token(pick_random_server)
        )

    # for dev.
    connection_index = 0 if not pick_random_server \
        else _random.randint(0, len(connection_urls) - 1)
    return pyArango.connection.Connection(
        arangoURL=connection_urls[connection_index],
        username=username, password=password
    )


CONNECTION = get_connection(
    _db_settings.USERNAME, _db_settings.PASSWORD, _db_settings.CONNECTION_URLS
)
