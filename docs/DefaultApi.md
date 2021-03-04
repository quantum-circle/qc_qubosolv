# qc_qubosolv_api.DefaultApi

All URIs are relative to *https://annealer.quantum-circle.com*

Method | HTTP request | Description
------------- | ------------- | -------------
[**heartbeat_get**](DefaultApi.md#heartbeat_get) | **GET** /heartbeat | 


# **heartbeat_get**
> object heartbeat_get()



### Example
```python
from __future__ import print_function
import time
import qc_qubosolv_api
from qc_qubosolv_api.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = qc_qubosolv_api.DefaultApi()

try:
    api_response = api_instance.heartbeat_get()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DefaultApi->heartbeat_get: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

**object**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

