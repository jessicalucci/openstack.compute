import mock
import cloudservers
import cloudservers.exceptions
import httplib2
from nose.tools import *

def test_authenticate_success():
    cs = cloudservers.CloudServers("username", "apikey")
    auth_response = httplib2.Response({
        'status': 204,
        'x-server-management-url': 'https://servers.api.rackspacecloud.com/v1.0/443470',
        'x-auth-token': '1b751d74-de0c-46ae-84f0-915744b582d1',
    })
    mock_request = mock.Mock(return_value=(auth_response, None))
    with mock.patch_object(httplib2.Http, "request", mock_request):
        cs.client.authenticate()
        mock_request.assert_called_with(cs.client.AUTH_URL, 'GET', 
            headers={'X-Auth-User': 'username', 'X-Auth-Key': 'apikey'})
        assert_equal(cs.client.management_url, auth_response['x-server-management-url'])
        assert_equal(cs.client.auth_token, auth_response['x-auth-token'])

def test_authenticate_failure():
    cs = cloudservers.CloudServers("username", "apikey")
    auth_response = httplib2.Response({'status': 401})
    mock_request = mock.Mock(return_value=(auth_response, None))
    with mock.patch_object(httplib2.Http, "request", mock_request):
        assert_raises(cloudservers.exceptions.Unauthorized, cs.client.authenticate)