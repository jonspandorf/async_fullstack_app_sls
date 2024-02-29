import axios from 'axios'

export const getPresignedUrl = async (filename) => {
  try {
    const res = await axios.get(`/api/upload?filename=${filename}`)
    return res.data.presignedUrl
  } catch (err) {
    console.error(err)
  }
}

export const uploadFileToBucket = async (presignedUrl, formData) => {

    try {
        const res = await axios.put(presignedUrl, formData.get('image'), {
            headers: {
              "Content-Type": "image/jpeg",
            },
          })
          return res
    } catch (err) {
        console.error(err)
    }

}