import logo from './logo.svg';
import './App.css';

import { useEffect, useState } from 'react';
import { Button, Col, Container, Form, Image, Row, Spinner} from 'react-bootstrap'
import { getPresignedUrl, uploadFileToBucket } from './api';
import { useArtifactChecker } from './wss';



function App() {


  const [ file, setFile ] = useState(null)
  const [ filename, setFilename ] = useState("")
  const [ imageUrl, setImageUrl ] = useState("")
  const [ isSubmitting, setSubmitting ] = useState(false) 
  const [ readyToCheck, setReadyToCheck ] = useState(false)
  const processedImageUrl = useArtifactChecker(filename+'Processed', readyToCheck)




  useEffect(() => {
    if (readyToCheck) {
      if (processedImageUrl) {
        setSubmitting(false)
        setImageUrl(processedImageUrl)
      }
    }

  }, [readyToCheck, processedImageUrl])

  const handleImageSelection = async (e) => {
    await new Promise((res) => res(setFile(e.target.files[0])));
    console.log(e.target.files[0])
    setImageUrl(URL.createObjectURL(e.target.files[0]))

  }

  const handleUpload = async (e) => {
    e.preventDefault()
    const formData = new FormData();
    formData.append('image', file)
    setSubmitting(true)
    const presigendUrl = await getPresignedUrl(filename)
    await uploadFileToBucket(presigendUrl, formData)
    await new Promise((res) => setTimeout(res,25))
    console.log('checking if ready')
    setReadyToCheck(true)
  }


  return (
    <Container className="d-flex justify-content-center align-items-center" style={{ minHeight: '100vh' }}>
      <Row>
        <Col>
          <Form onSubmit={handleUpload}>
          <Form.Group controlId="formFileName">
            <Form.Label>Filename</Form.Label>
              <Form.Control
                type="text"
                placeholder="Enter file name"
                value={filename}
                onChange={(e) => setFilename(e.target.value)}
              />
              <Form.Text className="text-muted">
                Please enter the desired file name.
              </Form.Text>
          </Form.Group>
            <Form.Group controlId="formFileLg" className="mb-3">
              <Form.Label>Upload an Image with faces</Form.Label>
              <Form.Control type="file" size="lg" onChange={handleImageSelection}/>
            </Form.Group>
              <div className="d-flex justify-content-center align-items-center">
                <Button variant="primary" type="submit" disabled={isSubmitting}>
                    {isSubmitting ? <Spinner animation="border" size="sm" /> : 'Upload'}
                </Button>
              </div>
            </Form>
          { imageUrl && <Image src={imageUrl} fluid />}
        </Col>
      </Row>
  </Container>
  );
}

export default App;
