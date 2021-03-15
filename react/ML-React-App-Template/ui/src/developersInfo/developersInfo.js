import React, { Component } from 'react';
import './developersInfo.css';
import Form from 'react-bootstrap/Form';
import Col from 'react-bootstrap/Col';
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Button from 'react-bootstrap/Button';
import 'bootstrap/dist/css/bootstrap.css';

export default class DevelopersInfo extends Component {

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
    fetch('http://127.0.0.1:5000/prediction1/', 
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
      <Container>
        <div>
          <h1 className="title">About</h1>
        </div>
        <div className="content">
          <p className = "texthelp">
            This app is made for the purpose of making the evaluation process easier to assist the instructors
            in  grading answer sheets after a thorough plagiarism, semantic and entailment analysis and thus saving their valuable time. This app can be 
            easily used for analysing test based examination of hundreds or thousands of students.
          </p>

          <p className = "texthelp">
            We are thankful to our instructors, <a href ="https://sites.google.com/site/romibitsnbob"> Dr. Romi Banerjee </a> and <a href ="https://iitj.irins.org/profile/94309"> Dr. Debarati Bhunia Chakraborty </a> for providing us the 
            necessary guidance, without which we would have not been able to complete this work. We heartily appreciate the much needed support and the help throughout the course of the project.
          </p>
          <p className = "texthelp" >
            Currently, we are two B-Tech students at IIT Jodhpur, <a href= "https://adityag5582.github.io/adityag5582/"> Aditya 
            Kumar </a> and <a href = "https://vyaskartik20.github.io/"> Kartik Vyas</a>, interested in good and new technology with an aim to learn the things that make life easier
            for people. We have used several machine learning algorithms, trained several models using different datasets, all the work along with the code, demo, and reports can be referred to at the
             <a href="https://github.com/vyaskartik20/Semantic_Plagiarism_Checker_for_Handwritten_Scripts"> github repository</a>.
          </p>
        </div>

        {/* <a href="google.com" URL> Google </a> <!-- link to site --> */}

      </Container>
    );
  }
}
