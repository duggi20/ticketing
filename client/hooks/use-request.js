import axios from 'axios'
import { useState } from 'react'

const useRequest = ({ url, method, body, onSuccess }) => {
  const [errors, setErrors] = useState(null)

  const request = async (requestBody = body) => {
    try {
      setErrors(null)
      const response = await axios[method](url, requestBody)
      console.log('response', response)
      if (onSuccess) {
        onSuccess(response.data)
      }
      return response.data
    } catch (err) {
      console.log("err",err)
      if(err && err[0] && err[0].message) {
        setErrors(err[0].message)
      }
      if(err.response && err.response.data && err.response.data.errors) {
          setErrors(err.response.data.errors)
      }

    }
  }

  return { request, errors }
}

export default useRequest
