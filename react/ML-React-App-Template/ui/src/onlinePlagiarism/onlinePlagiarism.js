import React, { Component } from 'react';
import './onlinePlagiarism.css';
import Form from 'react-bootstrap/Form';
import Col from 'react-bootstrap/Col';
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Button from 'react-bootstrap/Button';
import 'bootstrap/dist/css/bootstrap.css';
import { makeStyles } from '@material-ui/core/styles';
import Background from './images/3.jfif';

// const useStyles = makeStyles((theme) => ({
  
//   root: {
//     backgroundImage: `url(${Background})`,
//     // backgroundRepeat: 'no-repeat',
//     backgroundColor:
//       theme.palette.type === 'light' ? theme.palette.grey[50] : theme.palette.grey[900],
//       backgroundPosition: 'center',
//     backgroundSize: 'cover',
//     // height : '100%',
//     width : '100%',
//     // backgroundAttachment : 'fixed'
//   }
// }));

export default class OnlinePlagiarism extends Component {

  constructor(props) {
    super(props);

    this.state = {
      isLoading: false,
      formData: {
        textfield1: '',
        textfield2: '',
        select1: 1,
        select2: 1,
        select3: 1
      },
      result: ""
    };
  }

  handleChange = (event) => {
    const value = event.target.value;
    const name = event.target.name;
    var formData = this.state.formData;
    formData[name] = value;
    this.setState({
      formData
    });
  }

  handlePredictClick = (event) => {
    const formData = this.state.formData;
    this.setState({ isLoading: true });
    fetch('http://127.0.0.1:5000/predictionOnline/', 
      {
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json'
        },
        method: 'POST',
        body: JSON.stringify(formData)
      })
      .then(response => response.json())
      .then(response => {
        this.setState({
          result: response.result,
          isLoading: false
        });
      });
  }

  handleCancelClick = (event) => {
   
    this.setState({ result: "",
                    formData : {
                      textfield1 : "",
                      textfield2 : ""
                    }
    });
  }

  render() {
    const isLoading = this.state.isLoading;
    const formData = this.state.formData;
    const result = this.state.result;

    return (
      <div style={{backgroundImage: `url(${Background})`,
        // backgroundPosition: 'center',
        backgroundSize: 'cover',
        height : '100%',
        width : '100%',
        backgroundAttachment : 'fixed',
        backgroundRepeat : 'no-repeat',
      }}
      >
      <Container style={{minHeight:'100vh'}} >
        <div>
          <h1 className="title">Online Plagiarism</h1>
        </div>
        <div className="content">
          <Form>
            <Form.Row>
              <Form.Group as={Col}>
                <center><Form.Label>Text Field</Form.Label></center>
                <Form.Control 
                  type="textarea" 
                  placeholder="Text Field" 
                  name="textfield1"
                  value={formData.textfield1}
                  onChange={this.handleChange} />
              </Form.Group>
              {/* <Form.Group as={Col}>
                <Form.Label>Text Field 2</Form.Label>
                <Form.Control 
                  type="textarea" 
                  placeholder="Text Field 2" 
                  name="textfield2"
                  value={formData.textfield2}
                  onChange={this.handleChange} />
              </Form.Group> */}
            </Form.Row>
            {/* <Form.Row>
              <Form.Group as={Col}>
                <Form.Label>Select 1</Form.Label>
                <Form.Control 
                  as="select"
                  value={formData.select1}
                  name="select1"
                  onChange={this.handleChange}>
                  <option>1</option>
                  <option>2</option>
                  <option>3</option>
                  <option>4</option>
                </Form.Control>
              </Form.Group>
              <Form.Group as={Col}>
                <Form.Label>Select 2</Form.Label>
                <Form.Control 
                  as="select"
                  value={formData.select2}
                  name="select2"
                  onChange={this.handleChange}>
                  <option>1</option>
                  <option>2</option>
                  <option>3</option>
                  <option>4</option>
                </Form.Control>
              </Form.Group>
              <Form.Group as={Col}>
                <Form.Label>Select 3</Form.Label>
                <Form.Control 
                  as="select"
                  value={formData.select3}
                  name="select3"
                  onChange={this.handleChange}>
                  <option>1</option>
                  <option>2</option>
                  <option>3</option>
                  <option>4</option>
                </Form.Control>
              </Form.Group>
            </Form.Row> */}
            <Row>
              <Col>
                <Button
                  block
                  variant="success"
                  disabled={isLoading}
                  onClick={!isLoading ? this.handlePredictClick : null}>
                  { isLoading ? 'Making prediction' : 'Predict' }
                </Button>
              </Col>
              <Col>
                <Button
                  block
                  variant="danger"
                  disabled={isLoading}
                  onClick={this.handleCancelClick}>
                  Reset prediction
                </Button>
              </Col>
            </Row>
          </Form>
          {result === "" ? null :
            (<Row>
              <Col className="result-container">
                <h5 id="result">{result}</h5>
              </Col>
            </Row>)
          }
        </div>
      </Container>
      </div>
    );
  }
}
