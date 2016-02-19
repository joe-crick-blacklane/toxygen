# -*- coding: utf-8 -*-
from ctypes import *
from platform import system
from toxcore_enums_and_consts import *
import os


class ToxOptions(Structure):
    _fields_ = [
        ('ipv6_enabled', c_bool),
        ('udp_enabled', c_bool),
        ('proxy_type', c_int),
        ('proxy_host', c_char_p),
        ('proxy_port', c_uint16),
        ('start_port', c_uint16),
        ('end_port', c_uint16),
        ('tcp_port', c_uint16),
        ('savedata_type', c_int),
        ('savedata_data', c_char_p),
        ('savedata_length', c_size_t)
    ]


class Tox(object):
    def __init__(self, *args):
        # load toxcore
        if system() == 'Linux':
            temp = os.path.dirname(os.path.abspath(__file__)) + '/libs/'
            os.chdir(temp)
            self.libtoxcore = CDLL(temp + 'libtoxcore.so')
        elif system() == 'Windows':
            self.libtoxcore = CDLL('libs/libtox.dll')
        else:
            raise OSError('Unknown system.')

        if len(args) == 2:
            # creating tox options struct
            tox_err_options = c_int()
            self.libtoxcore.tox_options_new.restype = POINTER(ToxOptions)
            self.tox_options = self.libtoxcore.tox_options_new(addressof(tox_err_options))
            if tox_err_options == TOX_ERR_OPTIONS_NEW['TOX_ERR_OPTIONS_NEW_MALLOC']:
                raise MemoryError('The function failed to allocate enough memory for the options struct.')

            # filling tox options struct
            savedata = args[0]
            settings = args[1]
            self.tox_options.contents.ipv6_enabled = settings['ipv6_enabled']
            self.tox_options.contents.udp_enabled = settings['udp_enabled']
            self.tox_options.contents.proxy_type = settings['proxy_type']
            self.tox_options.contents.proxy_host = settings['proxy_host']
            self.tox_options.contents.proxy_port = settings['proxy_port']
            self.tox_options.contents.start_port = settings['start_port']
            self.tox_options.contents.end_port = settings['end_port']
            self.tox_options.contents.tcp_port = settings['tcp_port']
            self.tox_options.contents.savedata_type = TOX_SAVEDATA_TYPE['TOX_SAVEDATA_TYPE_TOX_SAVE']
            self.tox_options.contents.savedata_data = c_char_p(savedata)
            self.tox_options.contents.savedata_length = len(savedata)

            # creating tox object
            tox_err = c_int()
            self.libtoxcore.tox_new.restype = POINTER(c_void_p)
            self._tox_pointer = self.libtoxcore.tox_new(self.tox_options, addressof(tox_err))
            if tox_err == TOX_ERR_NEW['TOX_ERR_NEW_NULL']:
                raise ArgumentError('One of the arguments to the function was NULL when it was not expected.')
            elif tox_err == TOX_ERR_NEW['TOX_ERR_NEW_MALLOC']:
                raise MemoryError('The function was unable to allocate enough '
                                  'memory to store the internal structures for the Tox object.')
            elif tox_err == TOX_ERR_NEW['TOX_ERR_NEW_PORT_ALLOC']:
                raise MemoryError('The function was unable to bind to a port. This may mean that all ports have already'
                                  ' been bound, e.g. by other Tox instances, or it may mean a permission error. You may'
                                  ' be able to gather more information from errno.')
            elif tox_err == TOX_ERR_NEW['TOX_ERR_NEW_PROXY_BAD_TYPE']:
                raise ArgumentError('proxy_type was invalid.')
            elif tox_err == TOX_ERR_NEW['TOX_ERR_NEW_PROXY_BAD_HOST']:
                raise ArgumentError('proxy_type was valid but the proxy_host passed had an invalid format or was NULL.')
            elif tox_err == TOX_ERR_NEW['TOX_ERR_NEW_PROXY_BAD_PORT']:
                raise ArgumentError('proxy_type was valid, but the proxy_port was invalid.')
            elif tox_err == TOX_ERR_NEW['TOX_ERR_NEW_PROXY_NOT_FOUND']:
                raise ArgumentError('The proxy address passed could not be resolved.')
            elif tox_err == TOX_ERR_NEW['TOX_ERR_NEW_LOAD_ENCRYPTED']:
                raise ArgumentError('The byte array to be loaded contained an encrypted save.')
            elif tox_err == TOX_ERR_NEW['TOX_ERR_NEW_LOAD_BAD_FORMAT']:
                raise ArgumentError('The data format was invalid. This can happen when loading data that was saved by'
                                    ' an older version of Tox, or when the data has been corrupted. When loading from'
                                    ' badly formatted data, some data may have been loaded, and the rest is discarded.'
                                    ' Passing an invalid length parameter also causes this error.')
        elif len(args) == 1:
            self._tox_pointer = args[0]
        else:
            raise ArgumentError('1 or 2 arguments expected')

    # -----------------------------------------------------------------------------------------------------------------
    # Creation and destruction
    # -----------------------------------------------------------------------------------------------------------------

    def get_savedata_size(self):
        return self.libtoxcore.tox_get_savedata_size(self._tox_pointer)

    def get_savedata(self, savedata=None):
        if savedata is None:
            savedata_size = self.get_savedata_size()
            savedata = create_string_buffer(savedata_size)
        self.libtoxcore.tox_get_savedata(self._tox_pointer, savedata)
        return savedata

    # -----------------------------------------------------------------------------------------------------------------
    # Connection lifecycle and event loop
    # -----------------------------------------------------------------------------------------------------------------

    def bootstrap(self, address, port, public_key):
        tox_err_bootstrap = c_int()
        result = self.libtoxcore.tox_bootstrap(self._tox_pointer, c_char_p(address), c_uint16(port),
                                               c_char_p(public_key), addressof(tox_err_bootstrap))
        if tox_err_bootstrap == TOX_ERR_BOOTSTRAP['TOX_ERR_BOOTSTRAP_OK']:
            return bool(result)
        elif tox_err_bootstrap == TOX_ERR_BOOTSTRAP['TOX_ERR_BOOTSTRAP_NULL']:
            raise ArgumentError('One of the arguments to the function was NULL when it was not expected.')
        elif tox_err_bootstrap == TOX_ERR_BOOTSTRAP['TOX_ERR_BOOTSTRAP_BAD_HOST']:
            raise ArgumentError('The address could not be resolved to an IP '
                                'address, or the IP address passed was invalid.')
        elif tox_err_bootstrap == TOX_ERR_BOOTSTRAP['TOX_ERR_BOOTSTRAP_BAD_PORT']:
            raise ArgumentError('The port passed was invalid. The valid port range is (1, 65535).')

    def add_tcp_relay(self, address, port, public_key):
        tox_err_bootstrap = c_int()
        result = self.libtoxcore.tox_add_tcp_relay(self._tox_pointer, c_char_p(address), c_uint16(port),
                                                   c_char_p(public_key), addressof(tox_err_bootstrap))
        if tox_err_bootstrap == TOX_ERR_BOOTSTRAP['TOX_ERR_BOOTSTRAP_OK']:
            return bool(result)
        elif tox_err_bootstrap == TOX_ERR_BOOTSTRAP['TOX_ERR_BOOTSTRAP_NULL']:
            raise ArgumentError('One of the arguments to the function was NULL when it was not expected.')
        elif tox_err_bootstrap == TOX_ERR_BOOTSTRAP['TOX_ERR_BOOTSTRAP_BAD_HOST']:
            raise ArgumentError('The address could not be resolved to an IP '
                                'address, or the IP address passed was invalid.')
        elif tox_err_bootstrap == TOX_ERR_BOOTSTRAP['TOX_ERR_BOOTSTRAP_BAD_PORT']:
            raise ArgumentError('The port passed was invalid. The valid port range is (1, 65535).')

    def self_get_connection_status(self):
        return self.libtoxcore.tox_self_get_connection_status(self._tox_pointer)

    def callback_self_connection_status(self, callback, user_data):
        tox_self_connection_status_cb = CFUNCTYPE(None, c_void_p, c_int, c_void_p)
        c_callback = tox_self_connection_status_cb(callback)
        self.libtoxcore.tox_callback_self_connection_status(self._tox_pointer, c_callback, c_void_p(user_data))

    def iteration_interval(self):
        return int(self.libtoxcore.tox_iteration_interval(self._tox_pointer).value)

    def iterate(self):
        self.libtoxcore.tox_iterate(self._tox_pointer)

    # -----------------------------------------------------------------------------------------------------------------
    # Internal client information (Tox address/id)
    # -----------------------------------------------------------------------------------------------------------------

    def self_get_address(self, address=None):
        if address is None:
            address = create_string_buffer(TOX_ADDRESS_SIZE)
        self.libtoxcore.tox_self_get_address(self._tox_pointer, address)
        return address

    def self_set_nospam(self, nospam):
        self.libtoxcore.tox_self_set_nospam(self._tox_pointer, c_uint32(nospam))

    def self_get_nospam(self):
        return int(self.libtoxcore.tox_self_get_nospam(self._tox_pointer).value)

    def self_get_public_key(self, public_key=None):
        if public_key is None:
            public_key = create_string_buffer(TOX_PUBLIC_KEY_SIZE)
        self.libtoxcore.tox_self_get_address(self._tox_pointer, public_key)
        return public_key

    def self_get_secret_key(self, secret_key=None):
        if secret_key is None:
            secret_key = create_string_buffer(TOX_PUBLIC_KEY_SIZE)
        self.libtoxcore.tox_self_get_secret_key(self._tox_pointer, secret_key)
        return secret_key

    # -----------------------------------------------------------------------------------------------------------------
    # User-visible client information (nickname/status)
    # -----------------------------------------------------------------------------------------------------------------

    def self_set_name(self, name, length):
        tox_err_set_info = c_int()
        result = self.libtoxcore.tox_self_set_name(self._tox_pointer, c_char_p(name),
                                                   c_size_t(length), addressof(tox_err_set_info))
        if tox_err_set_info == TOX_ERR_SET_INFO['TOX_ERR_SET_INFO_OK']:
            return bool(result)
        elif tox_err_set_info == TOX_ERR_SET_INFO['TOX_ERR_SET_INFO_NULL']:
            raise ArgumentError('One of the arguments to the function was NULL when it was not expected.')
        elif tox_err_set_info == TOX_ERR_SET_INFO['TOX_ERR_SET_INFO_TOO_LONG']:
            raise ArgumentError('Information length exceeded maximum permissible size.')

    def self_get_name_size(self):
        return int(self.libtoxcore.tox_self_get_name_size(self._tox_pointer).value)

    def self_get_name(self, name=None):
        if name is None:
            name = create_string_buffer(self.self_get_name_size())
        self.libtoxcore.tox_self_get_name(self._tox_pointer, name)
        return name

    def self_set_status_message(self, status_message, length):
        tox_err_set_info = c_int()
        result = self.libtoxcore.tox_self_set_status_message(self._tox_pointer, c_char_p(status_message),
                                                             c_size_t(length), addressof(tox_err_set_info))
        if tox_err_set_info == TOX_ERR_SET_INFO['TOX_ERR_SET_INFO_OK']:
            return bool(result)
        elif tox_err_set_info == TOX_ERR_SET_INFO['TOX_ERR_SET_INFO_NULL']:
            raise ArgumentError('One of the arguments to the function was NULL when it was not expected.')
        elif tox_err_set_info == TOX_ERR_SET_INFO['TOX_ERR_SET_INFO_TOO_LONG']:
            raise ArgumentError('Information length exceeded maximum permissible size.')

    def self_get_status_message_size(self):
        return int(self.libtoxcore.tox_self_get_status_message_size(self._tox_pointer).value)

    def self_get_status_message(self, status_message=None):
        if status_message is None:
            status_message = create_string_buffer(self.self_get_status_message_size())
        self.libtoxcore.tox_self_get_status_message(self._tox_pointer, status_message)
        return status_message

    def self_set_status(self, status):
        self.libtoxcore.tox_self_set_status(self._tox_pointer, c_int(status))

    def self_get_status(self):
        return self.libtoxcore.tox_self_get_status(self._tox_pointer)

    # -----------------------------------------------------------------------------------------------------------------
    # Friend list management
    # -----------------------------------------------------------------------------------------------------------------

    def friend_add(self, address, message, length):
        tox_err_friend_add = c_int()
        result = self.libtoxcore.tox_friend_add(self._tox_pointer, c_char_p(address), c_char_p(message),
                                                c_size_t(length), addressof(tox_err_friend_add))
        if tox_err_friend_add == TOX_ERR_FRIEND_ADD['TOX_ERR_FRIEND_ADD_OK']:
            return int(result.value)
        elif tox_err_friend_add == TOX_ERR_FRIEND_ADD['TOX_ERR_FRIEND_ADD_NULL']:
            raise ArgumentError('One of the arguments to the function was NULL when it was not expected.')
        elif tox_err_friend_add == TOX_ERR_FRIEND_ADD['TOX_ERR_FRIEND_ADD_TOO_LONG']:
            raise ArgumentError('The length of the friend request message exceeded TOX_MAX_FRIEND_REQUEST_LENGTH.')
        elif tox_err_friend_add == TOX_ERR_FRIEND_ADD['TOX_ERR_FRIEND_ADD_NO_MESSAGE']:
            raise ArgumentError('The friend request message was empty. This, and the TOO_LONG code will never be'
                                ' returned from tox_friend_add_norequest.')
        elif tox_err_friend_add == TOX_ERR_FRIEND_ADD['TOX_ERR_FRIEND_ADD_OWN_KEY']:
            raise ArgumentError('The friend address belongs to the sending client.')
        elif tox_err_friend_add == TOX_ERR_FRIEND_ADD['TOX_ERR_FRIEND_ADD_ALREADY_SENT']:
            raise ArgumentError('A friend request has already been sent, or the address belongs to a friend that is'
                                ' already on the friend list.')
        elif tox_err_friend_add == TOX_ERR_FRIEND_ADD['TOX_ERR_FRIEND_ADD_BAD_CHECKSUM']:
            raise ArgumentError('The friend address checksum failed.')
        elif tox_err_friend_add == TOX_ERR_FRIEND_ADD['TOX_ERR_FRIEND_ADD_SET_NEW_NOSPAM']:
            raise ArgumentError('The friend was already there, but the nospam value was different.')
        elif tox_err_friend_add == TOX_ERR_FRIEND_ADD['TOX_ERR_FRIEND_ADD_MALLOC']:
            raise MemoryError('A memory allocation failed when trying to increase the friend list size.')

    def friend_add_norequest(self, public_key):
        tox_err_friend_add = c_int()
        result = self.libtoxcore.tox_friend_add(self._tox_pointer, c_char_p(public_key), addressof(tox_err_friend_add))
        if tox_err_friend_add == TOX_ERR_FRIEND_ADD['TOX_ERR_FRIEND_ADD_OK']:
            return int(result.value)
        elif tox_err_friend_add == TOX_ERR_FRIEND_ADD['TOX_ERR_FRIEND_ADD_NULL']:
            raise ArgumentError('One of the arguments to the function was NULL when it was not expected.')
        elif tox_err_friend_add == TOX_ERR_FRIEND_ADD['TOX_ERR_FRIEND_ADD_TOO_LONG']:
            raise ArgumentError('The length of the friend request message exceeded TOX_MAX_FRIEND_REQUEST_LENGTH.')
        elif tox_err_friend_add == TOX_ERR_FRIEND_ADD['TOX_ERR_FRIEND_ADD_NO_MESSAGE']:
            raise ArgumentError('The friend request message was empty. This, and the TOO_LONG code will never be'
                                ' returned from tox_friend_add_norequest.')
        elif tox_err_friend_add == TOX_ERR_FRIEND_ADD['TOX_ERR_FRIEND_ADD_OWN_KEY']:
            raise ArgumentError('The friend address belongs to the sending client.')
        elif tox_err_friend_add == TOX_ERR_FRIEND_ADD['TOX_ERR_FRIEND_ADD_ALREADY_SENT']:
            raise ArgumentError('A friend request has already been sent, or the address belongs to a friend that is'
                                ' already on the friend list.')
        elif tox_err_friend_add == TOX_ERR_FRIEND_ADD['TOX_ERR_FRIEND_ADD_BAD_CHECKSUM']:
            raise ArgumentError('The friend address checksum failed.')
        elif tox_err_friend_add == TOX_ERR_FRIEND_ADD['TOX_ERR_FRIEND_ADD_SET_NEW_NOSPAM']:
            raise ArgumentError('The friend was already there, but the nospam value was different.')
        elif tox_err_friend_add == TOX_ERR_FRIEND_ADD['TOX_ERR_FRIEND_ADD_MALLOC']:
            raise MemoryError('A memory allocation failed when trying to increase the friend list size.')

    def friend_delete(self, friend_number):
        tox_err_friend_delete = c_int()
        result = self.libtoxcore.tox_friend_delete(self._tox_pointer, c_uint32(friend_number),
                                                   addressof(tox_err_friend_delete))
        if tox_err_friend_delete == TOX_ERR_FRIEND_DELETE['TOX_ERR_FRIEND_DELETE_OK']:
            return bool(result)
        elif tox_err_friend_delete == TOX_ERR_FRIEND_DELETE['TOX_ERR_FRIEND_DELETE_FRIEND_NOT_FOUND']:
            raise ArgumentError('There was no friend with the given friend number. No friends were deleted.')

    # -----------------------------------------------------------------------------------------------------------------
    # Friend list queries
    # -----------------------------------------------------------------------------------------------------------------

    def friend_by_public_key(self, public_key):
        tox_err_friend_by_public_key = c_int()
        result = self.libtoxcore.tox_friend_by_public_key(self._tox_pointer, c_char_p(public_key),
                                                          addressof(tox_err_friend_by_public_key))
        if tox_err_friend_by_public_key == TOX_ERR_FRIEND_BY_PUBLIC_KEY['TOX_ERR_FRIEND_BY_PUBLIC_KEY_OK']:
            return int(result.value)
        elif tox_err_friend_by_public_key == TOX_ERR_FRIEND_BY_PUBLIC_KEY['TOX_ERR_FRIEND_BY_PUBLIC_KEY_NULL']:
            raise ArgumentError('One of the arguments to the function was NULL when it was not expected.')
        elif tox_err_friend_by_public_key == TOX_ERR_FRIEND_BY_PUBLIC_KEY['TOX_ERR_FRIEND_BY_PUBLIC_KEY_NOT_FOUND']:
            raise ArgumentError('No friend with the given Public Key exists on the friend list.')

    def friend_exists(self, friend_number):
        return bool(self.libtoxcore.tox_friend_by_public_key(self._tox_pointer, c_uint32(friend_number)))

    def self_get_friend_list_size(self):
        return int(self.libtoxcore.tox_self_get_friend_list_size(self._tox_pointer).value)

    def self_get_friend_list(self, friend_list=None):
        if friend_list is None:
            friend_list = create_string_buffer(sizeof(c_uint32) * self.self_get_friend_list_size())
            friend_list = POINTER(c_uint32)(friend_list)
        self.libtoxcore.tox_self_get_friend_list(self._tox_pointer, friend_list)
        return friend_list

    def friend_get_public_key(self, friend_number, public_key):
        tox_err_friend_get_public_key = c_int()
        result = self.libtoxcore.tox_friend_get_public_key(self._tox_pointer, c_uint32(friend_number),
                                                           c_char_p(public_key),
                                                           addressof(tox_err_friend_get_public_key))
        if tox_err_friend_get_public_key == TOX_ERR_FRIEND_GET_PUBLIC_KEY['TOX_ERR_FRIEND_GET_PUBLIC_KEY_OK']:
            return bool(result)
        elif tox_err_friend_get_public_key == TOX_ERR_FRIEND_GET_PUBLIC_KEY['TOX_ERR_FRIEND_GET_PUBLIC_KEY_FRIEND_NOT_FOUND']:
            raise ArgumentError('No friend with the given number exists on the friend list.')

    def friend_get_last_online(self, friend_number):
        tox_err_last_online = c_int()
        result = self.libtoxcore.tox_friend_get_last_online(self._tox_pointer, c_uint32(friend_number),
                                                            addressof(tox_err_last_online))
        if tox_err_last_online == TOX_ERR_FRIEND_GET_LAST_ONLINE['TOX_ERR_FRIEND_GET_LAST_ONLINE_OK']:
            return int(result.value)
        elif tox_err_last_online == TOX_ERR_FRIEND_GET_LAST_ONLINE['TOX_ERR_FRIEND_GET_LAST_ONLINE_FRIEND_NOT_FOUND']:
            raise ArgumentError('No friend with the given number exists on the friend list.')

    # -----------------------------------------------------------------------------------------------------------------
    # Friend-specific state queries (can also be received through callbacks)
    # -----------------------------------------------------------------------------------------------------------------

    def friend_get_name_size(self, friend_number):
        tox_err_friend_query = c_int()
        result = self.libtoxcore.tox_friend_get_name_size(self._tox_pointer, c_uint32(friend_number),
                                                          addressof(tox_err_friend_query))
        if tox_err_friend_query == TOX_ERR_FRIEND_QUERY['TOX_ERR_FRIEND_QUERY_OK']:
            return int(result.value)
        elif tox_err_friend_query == TOX_ERR_FRIEND_QUERY['TOX_ERR_FRIEND_QUERY_NULL']:
            raise ArgumentError('The pointer parameter for storing the query result (name, message) was NULL. Unlike'
                                ' the `_self_` variants of these functions, which have no effect when a parameter is'
                                ' NULL, these functions return an error in that case.')
        elif tox_err_friend_query == TOX_ERR_FRIEND_QUERY['TOX_ERR_FRIEND_QUERY_FRIEND_NOT_FOUND']:
            raise ArgumentError('The friend_number did not designate a valid friend.')

    def friend_get_name(self, friend_number, name):
        tox_err_friend_query = c_int()
        result = self.libtoxcore.tox_friend_get_name(self._tox_pointer, c_uint32(friend_number), name,
                                                     addressof(tox_err_friend_query))
        if tox_err_friend_query == TOX_ERR_FRIEND_QUERY['TOX_ERR_FRIEND_QUERY_OK']:
            return bool(result)
        elif tox_err_friend_query == TOX_ERR_FRIEND_QUERY['TOX_ERR_FRIEND_QUERY_NULL']:
            raise ArgumentError('The pointer parameter for storing the query result (name, message) was NULL. Unlike'
                                ' the `_self_` variants of these functions, which have no effect when a parameter is'
                                ' NULL, these functions return an error in that case.')
        elif tox_err_friend_query == TOX_ERR_FRIEND_QUERY['TOX_ERR_FRIEND_QUERY_FRIEND_NOT_FOUND']:
            raise ArgumentError('The friend_number did not designate a valid friend.')

    def callback_friend_name(self, callback, user_data):
        tox_friend_name_cb = CFUNCTYPE(None, c_void_p, c_uint32, c_char_p, c_size_t, c_void_p)
        c_callback = tox_friend_name_cb(callback)
        self.libtoxcore.tox_callback_friend_name(self._tox_pointer, c_callback, c_void_p(user_data))

    def friend_get_status_message_size(self, friend_number):
        tox_err_friend_query = c_int()
        result = self.libtoxcore.tox_friend_get_status_message_size(self._tox_pointer, c_uint32(friend_number),
                                                                    addressof(tox_err_friend_query))
        if tox_err_friend_query == TOX_ERR_FRIEND_QUERY['TOX_ERR_FRIEND_QUERY_OK']:
            return int(result.value)
        elif tox_err_friend_query == TOX_ERR_FRIEND_QUERY['TOX_ERR_FRIEND_QUERY_NULL']:
            raise ArgumentError('The pointer parameter for storing the query result (name, message) was NULL. Unlike'
                                ' the `_self_` variants of these functions, which have no effect when a parameter is'
                                ' NULL, these functions return an error in that case.')
        elif tox_err_friend_query == TOX_ERR_FRIEND_QUERY['TOX_ERR_FRIEND_QUERY_FRIEND_NOT_FOUND']:
            raise ArgumentError('The friend_number did not designate a valid friend.')

    def friend_get_status_message(self, friend_number, status_message):
        tox_err_friend_query = c_int()
        result = self.libtoxcore.tox_friend_get_status_message(self._tox_pointer, c_uint32(friend_number),
                                                               status_message, addressof(tox_err_friend_query))
        if tox_err_friend_query == TOX_ERR_FRIEND_QUERY['TOX_ERR_FRIEND_QUERY_OK']:
            return bool(result)
        elif tox_err_friend_query == TOX_ERR_FRIEND_QUERY['TOX_ERR_FRIEND_QUERY_NULL']:
            raise ArgumentError('The pointer parameter for storing the query result (name, message) was NULL. Unlike'
                                ' the `_self_` variants of these functions, which have no effect when a parameter is'
                                ' NULL, these functions return an error in that case.')
        elif tox_err_friend_query == TOX_ERR_FRIEND_QUERY['TOX_ERR_FRIEND_QUERY_FRIEND_NOT_FOUND']:
            raise ArgumentError('The friend_number did not designate a valid friend.')

    def callback_friend_status_message(self, callback, user_data):
        friend_status_message_cb = CFUNCTYPE(None, c_void_p, c_uint32, c_char_p, c_size_t, c_void_p)
        c_callback = friend_status_message_cb(callback)
        self.libtoxcore.tox_callback_friend_status_message(self._tox_pointer, c_callback, c_void_p(user_data))

    def friend_get_status(self, friend_number):
        tox_err_friend_query = c_int()
        result = self.libtoxcore.tox_friend_get_status(self._tox_pointer, c_uint32(friend_number),
                                                       addressof(tox_err_friend_query))
        if tox_err_friend_query == TOX_ERR_FRIEND_QUERY['TOX_ERR_FRIEND_QUERY_OK']:
            return result
        elif tox_err_friend_query == TOX_ERR_FRIEND_QUERY['TOX_ERR_FRIEND_QUERY_NULL']:
            raise ArgumentError('The pointer parameter for storing the query result (name, message) was NULL. Unlike'
                                ' the `_self_` variants of these functions, which have no effect when a parameter is'
                                ' NULL, these functions return an error in that case.')
        elif tox_err_friend_query == TOX_ERR_FRIEND_QUERY['TOX_ERR_FRIEND_QUERY_FRIEND_NOT_FOUND']:
            raise ArgumentError('The friend_number did not designate a valid friend.')

    def callback_friend_status(self, callback, user_data):
        tox_friend_status_cb = CFUNCTYPE(None, c_void_p, c_uint32, c_int, c_void_p)
        c_callback = tox_friend_status_cb(callback)
        self.libtoxcore.tox_callback_friend_status(self._tox_pointer, c_callback, c_void_p(user_data))



    # -----------------------------------------------------------------------------------------------------------------
    # Sending private messages
    # -----------------------------------------------------------------------------------------------------------------

    def self_set_typing(self, friend_number, typing):
        tox_err_set_typing = c_int()
        result = self.libtoxcore.tox_friend_delete(self._tox_pointer, c_uint32(friend_number),
                                                   c_bool(typing), addressof(tox_err_set_typing))
        if tox_err_set_typing == TOX_ERR_SET_TYPING['TOX_ERR_SET_TYPING_OK']:
            return bool(result)
        elif tox_err_set_typing == TOX_ERR_SET_TYPING['TOX_ERR_SET_TYPING_FRIEND_NOT_FOUND']:
            raise ArgumentError('The friend number did not designate a valid friend.')

    def friend_send_message(self, friend_number, message_type, message, length):
        tox_err_friend_send_message = c_int()
        result = self.libtoxcore.tox_friend_send_message(self._tox_pointer, c_uint32(friend_number),
                                                         c_int(message_type), c_char_p(message), c_size_t(length),
                                                         addressof(tox_err_friend_send_message))
        if tox_err_friend_send_message == TOX_ERR_FRIEND_SEND_MESSAGE['TOX_ERR_FRIEND_SEND_MESSAGE_OK']:
            return int(result.value)
        elif tox_err_friend_send_message == TOX_ERR_FRIEND_SEND_MESSAGE['TOX_ERR_FRIEND_SEND_MESSAGE_NULL']:
            raise ArgumentError('One of the arguments to the function was NULL when it was not expected.')
        elif tox_err_friend_send_message == TOX_ERR_FRIEND_SEND_MESSAGE['TOX_ERR_FRIEND_SEND_MESSAGE_FRIEND_NOT_FOUND']:
            raise ArgumentError('The friend number did not designate a valid friend.')
        elif tox_err_friend_send_message == TOX_ERR_FRIEND_SEND_MESSAGE['TOX_ERR_FRIEND_SEND_MESSAGE_FRIEND_NOT_CONNECTED']:
            raise ArgumentError('This client is currently not connected to the friend.')
        elif tox_err_friend_send_message == TOX_ERR_FRIEND_SEND_MESSAGE['TOX_ERR_FRIEND_SEND_MESSAGE_SENDQ']:
            raise ArgumentError('An allocation error occurred while increasing the send queue size.')
        elif tox_err_friend_send_message == TOX_ERR_FRIEND_SEND_MESSAGE['TOX_ERR_FRIEND_SEND_MESSAGE_TOO_LONG']:
            raise ArgumentError('Message length exceeded TOX_MAX_MESSAGE_LENGTH.')
        elif tox_err_friend_send_message == TOX_ERR_FRIEND_SEND_MESSAGE['TOX_ERR_FRIEND_SEND_MESSAGE_EMPTY']:
            raise ArgumentError('Attempted to send a zero-length message.')

    def callback_friend_read_receipt(self, callback, user_data):
        tox_friend_read_receipt_cb = CFUNCTYPE(None, c_void_p, c_uint32, c_uint32, c_void_p)
        c_callback = tox_friend_read_receipt_cb(callback)
        self.libtoxcore.tox_callback_friend_read_receipt(self._tox_pointer, c_callback, c_void_p(user_data))

    def callback_friend_request(self, callback, user_data):
        tox_friend_request_cb = CFUNCTYPE(None, c_void_p, c_char_p, c_char_p, c_size_t, c_void_p)
        c_callback = tox_friend_request_cb(callback)
        self.libtoxcore.tox_callback_friend_request(self._tox_pointer, c_callback, c_void_p(user_data))

    def callback_friend_message(self, callback, user_data):
        tox_friend_message_cb = CFUNCTYPE(None, c_void_p, c_uint32, c_int, c_char_p, c_size_t, c_void_p)
        c_callback = tox_friend_message_cb(callback)
        self.libtoxcore.tox_callback_friend_message(self._tox_pointer, c_callback, c_void_p(user_data))

    # TODO File transmission: common between sending and receiving

    # TODO File transmission: sending

    # TODO File transmission: receiving

    # TODO Group chat management

    # TODO Group chat message sending and receiving

    # TODO Low-level custom packet sending and receiving

    # TODO Low-level network information

    def __del__(self):
        if hasattr(self, 'tox_options'):
            self.libtoxcore.tox_kill(self._tox_pointer)
            self.libtoxcore.tox_options_free(self.tox_options)


if __name__ == '__main__':
    c = c_uint64(24)
    c = int(c.value)
    print type(c)
    print(c)
