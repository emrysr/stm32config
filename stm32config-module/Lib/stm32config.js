
var stm32config = {
    /**
     * add new item
     * @return {object} promise
     */
    add: function(){
        return stm32config._fetch(path + "stm32config/create.json");
    },

    /**
     * delete item by id
     * @param {string|int} id of item to be removed
     * @return {object} ajax promise
     */
    remove: function(id){
        return stm32config._fetch({
            url: path + "stm32config/delete.json",
            data: {id: id}
        });
    },
    /**
     * get all items
     * @return {object} ajax promise
     */
    list: function(){
        let url = path + "stm32config/list.json";
        let options = {}
        let promise = stm32config._fetch(url, options)
        promise.url = url;
        return promise;
    },
    /**
     * set new values for properites of an item
     * @param {object} options {properties,values,id}
     * @return {object} ajax promise
     */
    set: function(options) {
        return stm32config._fetch({
            url: path + "stm32config/set.json",
            data: {
                id: options.id,
                properties: options.properties,
                values: options.values,
            }
        });
    },
    /**
     * get a single property of an item
     * @param {object} options {properties,id}
     * @return {object} ajax promise
     */
    get: function(options) {
        return stm32config._fetch({
            url: path + "stm32config/get.json",
            data: {
                id: options.id,
                properties: options.properties
            }
        });
    },
    
    sample: function(options) {
        return stm32config._fetch({
            url: path + "stm32config/sample.json",
            data: {
                id: options.id
            }
        });
    },

    // AJAX UTILITIES
    // ---------------------

    /**
     * Send and test the response of an $.ajax request for error messages
     * 
     * Wrapper for $.ajax & tests for {success: false} in response
     * 
     * return standard $.ajax response
     * return failed $.ajax response if error message exists
     * 
     * @param: _fetch(settings)
     * @param: _fetch(url,[settings])
     * @see: https://api.jquery.com/jQuery.ajax/ for settings
     * @author: emrys@openenergymonitor.org
     */
    _fetch: function() {
        // call an api endpoint and return the callback queue
        var deferred = $.Deferred();
        var promise = deferred.promise();

        // if single object passed use that. else supply url and options
        var settings = arguments[0] || {};
        var jqxhr = null;
        
        // return rejected promise if no url passed
        if(!arguments[0]) deferred.reject(null, 'no url given');

        // if first parameter is string use that as the url
        if (typeof settings === 'string') {
            let url = arguments[0] || '';
            let settings = arguments[1] || {};
            jqxhr = $.ajax(url, settings);
        } else {
            jqxhr = $.ajax(settings);
        }

        // on ajax success check response for error message
        jqxhr.success(function(data, status, xhr) {
            // reject if data has property success set to false
            if (!data || data.hasOwnProperty('success') && data.success === false) {
                deferred.reject(jqxhr, data.message || 'error');
            } else {
                deferred.resolve(data, status, xhr);
            }
        });

        // on ajax error return rejected promise
        jqxhr.error(function(jqXHR, status, error) {
            deferred.reject(jqXHR, status, error);
        });
        
        return promise;
    }
}

