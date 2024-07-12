import axios from 'axios';

export const fetchApi = async (request) => {
  try {
    const response = await axios({ timeout: 5000, ...request });
    if (response.status >= 200 && response.status < 300) {
      // Successful response (2xx status code)
      return { isSuccess: true, errMessage: "", ...response.data };

    } else {
      // Non-2xx status code (e.g., 404, 500)
      return { isSuccess: false, errMessage: `return ${response.status} = ${response.statusText}` };
    }
  } catch (error) {
    if (error.response) {
      // The request was made, but the server responded with a non-2xx status code
      return { isSuccess: false, errMessage: `${error.response.status} = ${error.response.statusText}` };

    } else {
      // Something happened in setting up the request that triggered an error or timeout occurred
      return { isSuccess: false, errMessage: `${error.message}` };
    }
  }
};


export const apiGetStatus = async () => await fetchApi({ method: 'get', url:'/api/status' })
export const apiRequestStart = async (data) => await fetchApi({ method: 'put', url:'/api/start', data })
export const apiRequestStop = async () => await fetchApi({ method: 'put', url:'/api/stop' })
export const apiRequestReset = async () => await fetchApi({ method: 'put', url:'/api/reset' })
export const apiRequestTest = async () => await fetchApi({ method: 'put', url:'/api/test' })
