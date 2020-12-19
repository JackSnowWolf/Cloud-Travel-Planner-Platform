/*
 * Copyright 2010-2016 Amazon.com, Inc. or its affiliates. All Rights Reserved.
 *
 * Licensed under the Apache License, Version 2.0 (the "License").
 * You may not use this file except in compliance with the License.
 * A copy of the License is located at
 *
 *  http://aws.amazon.com/apache2.0
 *
 * or in the "license" file accompanying this file. This file is distributed
 * on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
 * express or implied. See the License for the specific language governing
 * permissions and limitations under the License.
 */

var apigClientFactory = {};
apigClientFactory.newClient = function (config) {
    var apigClient = { };
    if(config === undefined) {
        config = {
            accessKey: '',
            secretKey: '',
            sessionToken: '',
            region: 'us-east1',
            apiKey: undefined,
            defaultContentType: 'application/json',
            defaultAcceptType: 'application/json'
        };
    }
    if(config.accessKey === undefined) {
        config.accessKey = '';
    }
    if(config.secretKey === undefined) {
        config.secretKey = '';
    }
    if(config.apiKey === undefined) {
        config.apiKey = '';
    }
    if(config.sessionToken === undefined) {
        config.sessionToken = '';
    }
    if(config.region === undefined) {
        config.region = 'us-east-1';
    }
    //If defaultContentType is not defined then default to application/json
    if(config.defaultContentType === undefined) {
        config.defaultContentType = 'application/json';
    }
    //If defaultAcceptType is not defined then default to application/json
    if(config.defaultAcceptType === undefined) {
        config.defaultAcceptType = 'application/json';
    }

    
    // extract endpoint and path from url
    var invokeUrl = 'https://n248ztw82a.execute-api.us-east-1.amazonaws.com/v1';
    var endpoint = /(^https?:\/\/[^\/]+)/g.exec(invokeUrl)[1];
    var pathComponent = invokeUrl.substring(endpoint.length);

    var sigV4ClientConfig = {
        accessKey: config.accessKey,
        secretKey: config.secretKey,
        sessionToken: config.sessionToken,
        serviceName: 'execute-api',
        region: config.region,
        endpoint: endpoint,
        defaultContentType: config.defaultContentType,
        defaultAcceptType: config.defaultAcceptType
    };

    var authType = 'NONE';
    if (sigV4ClientConfig.accessKey !== undefined && sigV4ClientConfig.accessKey !== '' && sigV4ClientConfig.secretKey !== undefined && sigV4ClientConfig.secretKey !== '') {
        authType = 'AWS_IAM';
    }

    var simpleHttpClientConfig = {
        endpoint: endpoint,
        defaultContentType: config.defaultContentType,
        defaultAcceptType: config.defaultAcceptType
    };

    var apiGatewayClient = apiGateway.core.apiGatewayClientFactory.newClient(simpleHttpClientConfig, sigV4ClientConfig);
    
    
    
    apigClient.acceptScheduleIdGet = function (params, body, additionalParams) {
        if(additionalParams === undefined) { additionalParams = {}; }
        
        apiGateway.core.utils.assertParametersDefined(params, ['scheduleId', 'editorId'], ['body']);
        
        var acceptScheduleIdGetRequest = {
            verb: 'get'.toUpperCase(),
            path: pathComponent + uritemplate('/accept/{scheduleId}').expand(apiGateway.core.utils.parseParametersToObject(params, ['scheduleId', ])),
            headers: apiGateway.core.utils.parseParametersToObject(params, []),
            queryParams: apiGateway.core.utils.parseParametersToObject(params, ['editorId']),
            body: body
        };
        
        
        return apiGatewayClient.makeRequest(acceptScheduleIdGetRequest, authType, additionalParams, config.apiKey);
    };
    
    
    apigClient.acceptScheduleIdOptions = function (params, body, additionalParams) {
        if(additionalParams === undefined) { additionalParams = {}; }
        
        apiGateway.core.utils.assertParametersDefined(params, [], ['body']);
        
        var acceptScheduleIdOptionsRequest = {
            verb: 'options'.toUpperCase(),
            path: pathComponent + uritemplate('/accept/{scheduleId}').expand(apiGateway.core.utils.parseParametersToObject(params, [])),
            headers: apiGateway.core.utils.parseParametersToObject(params, []),
            queryParams: apiGateway.core.utils.parseParametersToObject(params, []),
            body: body
        };
        
        
        return apiGatewayClient.makeRequest(acceptScheduleIdOptionsRequest, authType, additionalParams, config.apiKey);
    };
    
    
    apigClient.attractionSearchGet = function (params, body, additionalParams) {
        if(additionalParams === undefined) { additionalParams = {}; }
        
        apiGateway.core.utils.assertParametersDefined(params, ['pageNo', 'pageSize', 'q'], ['body']);
        
        var attractionSearchGetRequest = {
            verb: 'get'.toUpperCase(),
            path: pathComponent + uritemplate('/attraction/_search').expand(apiGateway.core.utils.parseParametersToObject(params, [])),
            headers: apiGateway.core.utils.parseParametersToObject(params, []),
            queryParams: apiGateway.core.utils.parseParametersToObject(params, ['pageNo', 'pageSize', 'q']),
            body: body
        };
        
        
        return apiGatewayClient.makeRequest(attractionSearchGetRequest, authType, additionalParams, config.apiKey);
    };
    
    
    apigClient.attractionSearchOptions = function (params, body, additionalParams) {
        if(additionalParams === undefined) { additionalParams = {}; }
        
        apiGateway.core.utils.assertParametersDefined(params, [], ['body']);
        
        var attractionSearchOptionsRequest = {
            verb: 'options'.toUpperCase(),
            path: pathComponent + uritemplate('/attraction/_search').expand(apiGateway.core.utils.parseParametersToObject(params, [])),
            headers: apiGateway.core.utils.parseParametersToObject(params, []),
            queryParams: apiGateway.core.utils.parseParametersToObject(params, []),
            body: body
        };
        
        
        return apiGatewayClient.makeRequest(attractionSearchOptionsRequest, authType, additionalParams, config.apiKey);
    };
    
    
    apigClient.chatbotPost = function (params, body, additionalParams) {
        if(additionalParams === undefined) { additionalParams = {}; }
        
        apiGateway.core.utils.assertParametersDefined(params, [], ['body']);
        
        var chatbotPostRequest = {
            verb: 'post'.toUpperCase(),
            path: pathComponent + uritemplate('/chatbot').expand(apiGateway.core.utils.parseParametersToObject(params, [])),
            headers: apiGateway.core.utils.parseParametersToObject(params, []),
            queryParams: apiGateway.core.utils.parseParametersToObject(params, []),
            body: body
        };
        
        
        return apiGatewayClient.makeRequest(chatbotPostRequest, authType, additionalParams, config.apiKey);
    };
    
    
    apigClient.chatbotOptions = function (params, body, additionalParams) {
        if(additionalParams === undefined) { additionalParams = {}; }
        
        apiGateway.core.utils.assertParametersDefined(params, [], ['body']);
        
        var chatbotOptionsRequest = {
            verb: 'options'.toUpperCase(),
            path: pathComponent + uritemplate('/chatbot').expand(apiGateway.core.utils.parseParametersToObject(params, [])),
            headers: apiGateway.core.utils.parseParametersToObject(params, []),
            queryParams: apiGateway.core.utils.parseParametersToObject(params, []),
            body: body
        };
        
        
        return apiGatewayClient.makeRequest(chatbotOptionsRequest, authType, additionalParams, config.apiKey);
    };
    
    
    apigClient.inviteUserIdGet = function (params, body, additionalParams) {
        if(additionalParams === undefined) { additionalParams = {}; }
        
        apiGateway.core.utils.assertParametersDefined(params, ['userId', 'scheduleId'], ['body']);
        
        var inviteUserIdGetRequest = {
            verb: 'get'.toUpperCase(),
            path: pathComponent + uritemplate('/invite/{userId}').expand(apiGateway.core.utils.parseParametersToObject(params, ['userId', ])),
            headers: apiGateway.core.utils.parseParametersToObject(params, []),
            queryParams: apiGateway.core.utils.parseParametersToObject(params, ['scheduleId']),
            body: body
        };
        
        
        return apiGatewayClient.makeRequest(inviteUserIdGetRequest, authType, additionalParams, config.apiKey);
    };
    
    
    apigClient.inviteUserIdOptions = function (params, body, additionalParams) {
        if(additionalParams === undefined) { additionalParams = {}; }
        
        apiGateway.core.utils.assertParametersDefined(params, [], ['body']);
        
        var inviteUserIdOptionsRequest = {
            verb: 'options'.toUpperCase(),
            path: pathComponent + uritemplate('/invite/{userId}').expand(apiGateway.core.utils.parseParametersToObject(params, [])),
            headers: apiGateway.core.utils.parseParametersToObject(params, []),
            queryParams: apiGateway.core.utils.parseParametersToObject(params, []),
            body: body
        };
        
        
        return apiGatewayClient.makeRequest(inviteUserIdOptionsRequest, authType, additionalParams, config.apiKey);
    };
    
    
    apigClient.scheduleGet = function (params, body, additionalParams) {
        if(additionalParams === undefined) { additionalParams = {}; }
        
        apiGateway.core.utils.assertParametersDefined(params, ['pageNo', 'pageSize'], ['body']);
        
        var scheduleGetRequest = {
            verb: 'get'.toUpperCase(),
            path: pathComponent + uritemplate('/schedule').expand(apiGateway.core.utils.parseParametersToObject(params, [])),
            headers: apiGateway.core.utils.parseParametersToObject(params, []),
            queryParams: apiGateway.core.utils.parseParametersToObject(params, ['pageNo', 'pageSize']),
            body: body
        };
        
        
        return apiGatewayClient.makeRequest(scheduleGetRequest, authType, additionalParams, config.apiKey);
    };
    
    
    apigClient.schedulePost = function (params, body, additionalParams) {
        if(additionalParams === undefined) { additionalParams = {}; }
        
        apiGateway.core.utils.assertParametersDefined(params, ['userId', 'targetArea', 'scheduleTitle'], ['body']);
        
        var schedulePostRequest = {
            verb: 'post'.toUpperCase(),
            path: pathComponent + uritemplate('/schedule').expand(apiGateway.core.utils.parseParametersToObject(params, [])),
            headers: apiGateway.core.utils.parseParametersToObject(params, []),
            queryParams: apiGateway.core.utils.parseParametersToObject(params, ['userId', 'targetArea', 'scheduleTitle']),
            body: body
        };
        
        
        return apiGatewayClient.makeRequest(schedulePostRequest, authType, additionalParams, config.apiKey);
    };
    
    
    apigClient.scheduleOptions = function (params, body, additionalParams) {
        if(additionalParams === undefined) { additionalParams = {}; }
        
        apiGateway.core.utils.assertParametersDefined(params, [], ['body']);
        
        var scheduleOptionsRequest = {
            verb: 'options'.toUpperCase(),
            path: pathComponent + uritemplate('/schedule').expand(apiGateway.core.utils.parseParametersToObject(params, [])),
            headers: apiGateway.core.utils.parseParametersToObject(params, []),
            queryParams: apiGateway.core.utils.parseParametersToObject(params, []),
            body: body
        };
        
        
        return apiGatewayClient.makeRequest(scheduleOptionsRequest, authType, additionalParams, config.apiKey);
    };
    
    
    apigClient.scheduleScheduleIdGet = function (params, body, additionalParams) {
        if(additionalParams === undefined) { additionalParams = {}; }
        
        apiGateway.core.utils.assertParametersDefined(params, ['scheduleId'], ['body']);
        
        var scheduleScheduleIdGetRequest = {
            verb: 'get'.toUpperCase(),
            path: pathComponent + uritemplate('/schedule/{scheduleId}').expand(apiGateway.core.utils.parseParametersToObject(params, ['scheduleId'])),
            headers: apiGateway.core.utils.parseParametersToObject(params, []),
            queryParams: apiGateway.core.utils.parseParametersToObject(params, []),
            body: body
        };
        
        
        return apiGatewayClient.makeRequest(scheduleScheduleIdGetRequest, authType, additionalParams, config.apiKey);
    };
    
    
    apigClient.scheduleScheduleIdPost = function (params, body, additionalParams) {
        if(additionalParams === undefined) { additionalParams = {}; }
        
        apiGateway.core.utils.assertParametersDefined(params, ['scheduleId', 'body'], ['body']);
        
        var scheduleScheduleIdPostRequest = {
            verb: 'post'.toUpperCase(),
            path: pathComponent + uritemplate('/schedule/{scheduleId}').expand(apiGateway.core.utils.parseParametersToObject(params, ['scheduleId', ])),
            headers: apiGateway.core.utils.parseParametersToObject(params, []),
            queryParams: apiGateway.core.utils.parseParametersToObject(params, []),
            body: body
        };
        
        
        return apiGatewayClient.makeRequest(scheduleScheduleIdPostRequest, authType, additionalParams, config.apiKey);
    };
    
    
    apigClient.scheduleScheduleIdDelete = function (params, body, additionalParams) {
        if(additionalParams === undefined) { additionalParams = {}; }
        
        apiGateway.core.utils.assertParametersDefined(params, ['scheduleId'], ['body']);
        
        var scheduleScheduleIdDeleteRequest = {
            verb: 'delete'.toUpperCase(),
            path: pathComponent + uritemplate('/schedule/{scheduleId}').expand(apiGateway.core.utils.parseParametersToObject(params, ['scheduleId'])),
            headers: apiGateway.core.utils.parseParametersToObject(params, []),
            queryParams: apiGateway.core.utils.parseParametersToObject(params, []),
            body: body
        };
        
        
        return apiGatewayClient.makeRequest(scheduleScheduleIdDeleteRequest, authType, additionalParams, config.apiKey);
    };
    
    
    apigClient.scheduleScheduleIdPatch = function (params, body, additionalParams) {
        if(additionalParams === undefined) { additionalParams = {}; }
        
        apiGateway.core.utils.assertParametersDefined(params, ['scheduleId', 'body'], ['body']);
        
        var scheduleScheduleIdPatchRequest = {
            verb: 'patch'.toUpperCase(),
            path: pathComponent + uritemplate('/schedule/{scheduleId}').expand(apiGateway.core.utils.parseParametersToObject(params, ['scheduleId', ])),
            headers: apiGateway.core.utils.parseParametersToObject(params, []),
            queryParams: apiGateway.core.utils.parseParametersToObject(params, []),
            body: body
        };
        
        
        return apiGatewayClient.makeRequest(scheduleScheduleIdPatchRequest, authType, additionalParams, config.apiKey);
    };
    
    
    apigClient.scheduleScheduleIdOptions = function (params, body, additionalParams) {
        if(additionalParams === undefined) { additionalParams = {}; }
        
        apiGateway.core.utils.assertParametersDefined(params, [], ['body']);
        
        var scheduleScheduleIdOptionsRequest = {
            verb: 'options'.toUpperCase(),
            path: pathComponent + uritemplate('/schedule/{scheduleId}').expand(apiGateway.core.utils.parseParametersToObject(params, [])),
            headers: apiGateway.core.utils.parseParametersToObject(params, []),
            queryParams: apiGateway.core.utils.parseParametersToObject(params, []),
            body: body
        };
        
        
        return apiGatewayClient.makeRequest(scheduleScheduleIdOptionsRequest, authType, additionalParams, config.apiKey);
    };
    
    
    apigClient.scheduleScheduleIdAttractionAttractionIdGet = function (params, body, additionalParams) {
        if(additionalParams === undefined) { additionalParams = {}; }
        
        apiGateway.core.utils.assertParametersDefined(params, ['scheduleId', 'attractionId'], ['body']);
        
        var scheduleScheduleIdAttractionAttractionIdGetRequest = {
            verb: 'get'.toUpperCase(),
            path: pathComponent + uritemplate('/schedule/{scheduleId}/attraction/{attractionId}').expand(apiGateway.core.utils.parseParametersToObject(params, ['scheduleId', 'attractionId'])),
            headers: apiGateway.core.utils.parseParametersToObject(params, []),
            queryParams: apiGateway.core.utils.parseParametersToObject(params, []),
            body: body
        };
        
        
        return apiGatewayClient.makeRequest(scheduleScheduleIdAttractionAttractionIdGetRequest, authType, additionalParams, config.apiKey);
    };
    
    
    apigClient.scheduleScheduleIdAttractionAttractionIdPut = function (params, body, additionalParams) {
        if(additionalParams === undefined) { additionalParams = {}; }
        
        apiGateway.core.utils.assertParametersDefined(params, ['scheduleId', 'attractionId'], ['body']);
        
        var scheduleScheduleIdAttractionAttractionIdPutRequest = {
            verb: 'put'.toUpperCase(),
            path: pathComponent + uritemplate('/schedule/{scheduleId}/attraction/{attractionId}').expand(apiGateway.core.utils.parseParametersToObject(params, ['scheduleId', 'attractionId'])),
            headers: apiGateway.core.utils.parseParametersToObject(params, []),
            queryParams: apiGateway.core.utils.parseParametersToObject(params, []),
            body: body
        };
        
        
        return apiGatewayClient.makeRequest(scheduleScheduleIdAttractionAttractionIdPutRequest, authType, additionalParams, config.apiKey);
    };
    
    
    apigClient.scheduleScheduleIdAttractionAttractionIdPost = function (params, body, additionalParams) {
        if(additionalParams === undefined) { additionalParams = {}; }
        
        apiGateway.core.utils.assertParametersDefined(params, ['scheduleId', 'attractionId'], ['body']);
        
        var scheduleScheduleIdAttractionAttractionIdPostRequest = {
            verb: 'post'.toUpperCase(),
            path: pathComponent + uritemplate('/schedule/{scheduleId}/attraction/{attractionId}').expand(apiGateway.core.utils.parseParametersToObject(params, ['scheduleId', 'attractionId'])),
            headers: apiGateway.core.utils.parseParametersToObject(params, []),
            queryParams: apiGateway.core.utils.parseParametersToObject(params, []),
            body: body
        };
        
        
        return apiGatewayClient.makeRequest(scheduleScheduleIdAttractionAttractionIdPostRequest, authType, additionalParams, config.apiKey);
    };
    
    
    apigClient.scheduleScheduleIdAttractionAttractionIdDelete = function (params, body, additionalParams) {
        if(additionalParams === undefined) { additionalParams = {}; }
        
        apiGateway.core.utils.assertParametersDefined(params, ['scheduleId', 'attractionId'], ['body']);
        
        var scheduleScheduleIdAttractionAttractionIdDeleteRequest = {
            verb: 'delete'.toUpperCase(),
            path: pathComponent + uritemplate('/schedule/{scheduleId}/attraction/{attractionId}').expand(apiGateway.core.utils.parseParametersToObject(params, ['scheduleId', 'attractionId'])),
            headers: apiGateway.core.utils.parseParametersToObject(params, []),
            queryParams: apiGateway.core.utils.parseParametersToObject(params, []),
            body: body
        };
        
        
        return apiGatewayClient.makeRequest(scheduleScheduleIdAttractionAttractionIdDeleteRequest, authType, additionalParams, config.apiKey);
    };
    
    
    apigClient.scheduleScheduleIdAttractionAttractionIdOptions = function (params, body, additionalParams) {
        if(additionalParams === undefined) { additionalParams = {}; }
        
        apiGateway.core.utils.assertParametersDefined(params, [], ['body']);
        
        var scheduleScheduleIdAttractionAttractionIdOptionsRequest = {
            verb: 'options'.toUpperCase(),
            path: pathComponent + uritemplate('/schedule/{scheduleId}/attraction/{attractionId}').expand(apiGateway.core.utils.parseParametersToObject(params, [])),
            headers: apiGateway.core.utils.parseParametersToObject(params, []),
            queryParams: apiGateway.core.utils.parseParametersToObject(params, []),
            body: body
        };
        
        
        return apiGatewayClient.makeRequest(scheduleScheduleIdAttractionAttractionIdOptionsRequest, authType, additionalParams, config.apiKey);
    };
    
    
    apigClient.scheduleScheduleIdDownloadGet = function (params, body, additionalParams) {
        if(additionalParams === undefined) { additionalParams = {}; }
        
        apiGateway.core.utils.assertParametersDefined(params, ['scheduleId'], ['body']);
        
        var scheduleScheduleIdDownloadGetRequest = {
            verb: 'get'.toUpperCase(),
            path: pathComponent + uritemplate('/schedule/{scheduleId}/download').expand(apiGateway.core.utils.parseParametersToObject(params, ['scheduleId'])),
            headers: apiGateway.core.utils.parseParametersToObject(params, []),
            queryParams: apiGateway.core.utils.parseParametersToObject(params, []),
            body: body
        };
        
        
        return apiGatewayClient.makeRequest(scheduleScheduleIdDownloadGetRequest, authType, additionalParams, config.apiKey);
    };
    
    
    apigClient.scheduleScheduleIdDownloadOptions = function (params, body, additionalParams) {
        if(additionalParams === undefined) { additionalParams = {}; }
        
        apiGateway.core.utils.assertParametersDefined(params, [], ['body']);
        
        var scheduleScheduleIdDownloadOptionsRequest = {
            verb: 'options'.toUpperCase(),
            path: pathComponent + uritemplate('/schedule/{scheduleId}/download').expand(apiGateway.core.utils.parseParametersToObject(params, [])),
            headers: apiGateway.core.utils.parseParametersToObject(params, []),
            queryParams: apiGateway.core.utils.parseParametersToObject(params, []),
            body: body
        };
        
        
        return apiGatewayClient.makeRequest(scheduleScheduleIdDownloadOptionsRequest, authType, additionalParams, config.apiKey);
    };
    
    
    apigClient.scheduleScheduleIdFinishGet = function (params, body, additionalParams) {
        if(additionalParams === undefined) { additionalParams = {}; }
        
        apiGateway.core.utils.assertParametersDefined(params, ['scheduleId'], ['body']);
        
        var scheduleScheduleIdFinishGetRequest = {
            verb: 'get'.toUpperCase(),
            path: pathComponent + uritemplate('/schedule/{scheduleId}/finish').expand(apiGateway.core.utils.parseParametersToObject(params, ['scheduleId'])),
            headers: apiGateway.core.utils.parseParametersToObject(params, []),
            queryParams: apiGateway.core.utils.parseParametersToObject(params, []),
            body: body
        };
        
        
        return apiGatewayClient.makeRequest(scheduleScheduleIdFinishGetRequest, authType, additionalParams, config.apiKey);
    };
    
    
    apigClient.scheduleScheduleIdFinishOptions = function (params, body, additionalParams) {
        if(additionalParams === undefined) { additionalParams = {}; }
        
        apiGateway.core.utils.assertParametersDefined(params, [], ['body']);
        
        var scheduleScheduleIdFinishOptionsRequest = {
            verb: 'options'.toUpperCase(),
            path: pathComponent + uritemplate('/schedule/{scheduleId}/finish').expand(apiGateway.core.utils.parseParametersToObject(params, [])),
            headers: apiGateway.core.utils.parseParametersToObject(params, []),
            queryParams: apiGateway.core.utils.parseParametersToObject(params, []),
            body: body
        };
        
        
        return apiGatewayClient.makeRequest(scheduleScheduleIdFinishOptionsRequest, authType, additionalParams, config.apiKey);
    };
    
    
    apigClient.scheduleScheduleIdSubmitGet = function (params, body, additionalParams) {
        if(additionalParams === undefined) { additionalParams = {}; }
        
        apiGateway.core.utils.assertParametersDefined(params, ['scheduleId'], ['body']);
        
        var scheduleScheduleIdSubmitGetRequest = {
            verb: 'get'.toUpperCase(),
            path: pathComponent + uritemplate('/schedule/{scheduleId}/submit').expand(apiGateway.core.utils.parseParametersToObject(params, ['scheduleId'])),
            headers: apiGateway.core.utils.parseParametersToObject(params, []),
            queryParams: apiGateway.core.utils.parseParametersToObject(params, []),
            body: body
        };
        
        
        return apiGatewayClient.makeRequest(scheduleScheduleIdSubmitGetRequest, authType, additionalParams, config.apiKey);
    };
    
    
    apigClient.scheduleScheduleIdSubmitPost = function (params, body, additionalParams) {
        if(additionalParams === undefined) { additionalParams = {}; }
        
        apiGateway.core.utils.assertParametersDefined(params, ['scheduleId'], ['body']);
        
        var scheduleScheduleIdSubmitPostRequest = {
            verb: 'post'.toUpperCase(),
            path: pathComponent + uritemplate('/schedule/{scheduleId}/submit').expand(apiGateway.core.utils.parseParametersToObject(params, ['scheduleId'])),
            headers: apiGateway.core.utils.parseParametersToObject(params, []),
            queryParams: apiGateway.core.utils.parseParametersToObject(params, []),
            body: body
        };
        
        
        return apiGatewayClient.makeRequest(scheduleScheduleIdSubmitPostRequest, authType, additionalParams, config.apiKey);
    };
    
    
    apigClient.scheduleScheduleIdSubmitOptions = function (params, body, additionalParams) {
        if(additionalParams === undefined) { additionalParams = {}; }
        
        apiGateway.core.utils.assertParametersDefined(params, [], ['body']);
        
        var scheduleScheduleIdSubmitOptionsRequest = {
            verb: 'options'.toUpperCase(),
            path: pathComponent + uritemplate('/schedule/{scheduleId}/submit').expand(apiGateway.core.utils.parseParametersToObject(params, [])),
            headers: apiGateway.core.utils.parseParametersToObject(params, []),
            queryParams: apiGateway.core.utils.parseParametersToObject(params, []),
            body: body
        };
        
        
        return apiGatewayClient.makeRequest(scheduleScheduleIdSubmitOptionsRequest, authType, additionalParams, config.apiKey);
    };
    
    
    apigClient.scheduleScheduleIdViewGet = function (params, body, additionalParams) {
        if(additionalParams === undefined) { additionalParams = {}; }
        
        apiGateway.core.utils.assertParametersDefined(params, ['scheduleId', 'fileType', 'accessKey'], ['body']);
        
        var scheduleScheduleIdViewGetRequest = {
            verb: 'get'.toUpperCase(),
            path: pathComponent + uritemplate('/schedule/{scheduleId}/view').expand(apiGateway.core.utils.parseParametersToObject(params, ['scheduleId', ])),
            headers: apiGateway.core.utils.parseParametersToObject(params, []),
            queryParams: apiGateway.core.utils.parseParametersToObject(params, ['fileType', 'accessKey']),
            body: body
        };
        
        
        return apiGatewayClient.makeRequest(scheduleScheduleIdViewGetRequest, authType, additionalParams, config.apiKey);
    };
    
    
    apigClient.scheduleScheduleIdViewOptions = function (params, body, additionalParams) {
        if(additionalParams === undefined) { additionalParams = {}; }
        
        apiGateway.core.utils.assertParametersDefined(params, [], ['body']);
        
        var scheduleScheduleIdViewOptionsRequest = {
            verb: 'options'.toUpperCase(),
            path: pathComponent + uritemplate('/schedule/{scheduleId}/view').expand(apiGateway.core.utils.parseParametersToObject(params, [])),
            headers: apiGateway.core.utils.parseParametersToObject(params, []),
            queryParams: apiGateway.core.utils.parseParametersToObject(params, []),
            body: body
        };
        
        
        return apiGatewayClient.makeRequest(scheduleScheduleIdViewOptionsRequest, authType, additionalParams, config.apiKey);
    };
    

    return apigClient;
};
