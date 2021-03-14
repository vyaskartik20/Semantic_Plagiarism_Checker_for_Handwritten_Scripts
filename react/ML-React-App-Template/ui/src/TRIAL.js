import React from 'react';
// import Avatar from '@material-ui/core/Avatar';
import Button from '@material-ui/core/Button';
import CssBaseline from '@material-ui/core/CssBaseline';
// import TextField from '@material-ui/core/TextField';
// import FormControlLabel from '@material-ui/core/FormControlLabel';
// import Checkbox from '@material-ui/core/Checkbox';
// import Link from '@material-ui/core/Link';
import Paper from '@material-ui/core/Paper';
// import Box from '@material-ui/core/Box';
import Grid from '@material-ui/core/Grid';
// import LockOutlinedIcon from '@material-ui/icons/LockOutlined';
import Typography from '@material-ui/core/Typography';
import { makeStyles } from '@material-ui/core/styles';
import AppBar from '@material-ui/core/AppBar';
import Toolbar from '@material-ui/core/Toolbar';
import {BrowserRouter as Router, Switch , Route} from 'react-router-dom';
import {Link} from 'react-router-dom';

// https://source.unsplash.com/random

import RealPlagiarism from './realPlagiarism/realPlagiarism';
import OnlinePlagiarism from './onlinePlagiarism/onlinePlagiarism';
import SemanticSimilarity from './semanticSimilarity/semanticSimilarity';
import EntailmentAnalysis from './entailmentAnalysis/entailmentAnalysis';
import Background from './images/coding20.jpg';


const useStyles = makeStyles((theme) => ({
  
  root: {
    height: '100vh  ',
  },
  image: {
    backgroundImage: 'url(https://picsum.photos/1000)',
    backgroundRepeat: 'no-repeat',
    backgroundColor:
      theme.palette.type === 'light' ? theme.palette.grey[50] : theme.palette.grey[900],
      backgroundPosition: 'center',
    backgroundSize: 'cover',
  },
  paper: {
    margin: theme.spacing(8, 4),
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    // backgroundColor:'black'
  },
  other: {
    // backgroundColor:'rgb(36,2,11)',
    // backgroundImage: require('./coding.jpg')
    // <img src={'./coding.jpg'} />
    // color:'white'
    backgroundImage: `url(${Background})`,
    backgroundRepeat: 'no-repeat',
    backgroundColor:
      theme.palette.type === 'light' ? theme.palette.grey[50] : theme.palette.grey[900],
      backgroundPosition: 'center',
    backgroundSize: 'cover',
  }
}));


// rgb(36,2,11)
// 82, 255, 128
// 255, 122, 235
// 82, 17, 72
// 26, 4, 22

// const classes = useStyles();

export default function App() {
  
  return (
    // <Pomodoro/>
    // <Pomodoro/>
    // <OnlinePlagiarism />
    <Router>
      <div>
        <Switch>
          <Route path="/real" component={RealPlagiarism} />
          <Route path="/online" component={OnlinePlagiarism} />
          <Route path="/semantic" component={SemanticSimilarity} />
          <Route path="/entailment" component={EntailmentAnalysis} />
          <Route path="/" component={Home} />
        </Switch>
      </div>
    </Router>
    
  );
}
  
  
  const Home =() => (

    // <Grid container component="main">
    //   <CssBaseline />
    //   <Grid item xs={false} sm={4} md={6} />
    //   <Grid item xs={12} sm={8} md={6}  component={Paper} elevation={6} square>
    //     <div >
    //       {/* <Button
    //         type="submit"
    //         fullWidth
    //         variant="contained"
    //         color="primary"
    //         className={classes.submit}
    //       >
    //         Sign In
    //       </Button>
    //        */}
    //       <AppBar position="static"  style={{ background: 'inherit' }} >
    //         <Toolbar>
    //           <Typography variant="h3" style={{color:'rgb(26,80,22)'}} >
    //             Pacify 
    //           </Typography>
    //         </Toolbar>
    //       </AppBar>
    //       <div style={{ marginTop:'18%', marginBottom:'6%' ,width: '40%' }} >
    //         <Button variant="contained" size="large" style={{width: '100%',color:'red', backgroundColor:'white'}} href="Compiler">
    //           Compiler
    //         </Button>
    //       </div>
    //       <div style={{margin:'6%',width: '40%' }}>
    //         <Button variant="contained" size="large" style={{width: '100%',color:'red', backgroundColor:'white'}} href="#contained-buttons">
    //           Test Case Genreator
    //         </Button>
    //       </div>
    //       <div style={{margin:'6%',width: '40%'}}>
    //         <Button variant="contained" size="large" style={{width: '100%' ,color:'red', backgroundColor:'white'}}  href="#contained-buttons">
    //           Debugger
    //         </Button>
    //       </div>
    //       {/* <div></div> */}
    //       <div style={{alignSelf:'flex-end', justifyContent:'space-between', marginTop:'6%'}}>
    //         <h3 style={{color:'white'}}>
    //           Developed by Kartik and Aditya 
    //         </h3>
    //       </div>
    //     </div>
    //   </Grid>
    //   {/* <Grid item xs={false} sm={4} md={4} className={classes.image} /> */}
    // </Grid>



  <Grid container component="main" className={useStyles().root}>
      <CssBaseline />
      <Grid item xs={false} sm={4} md={6} className={useStyles().image} />
      <Grid item xs={12} sm={8} md={6} className={useStyles().other} component={Paper} elevation={6} square>
        <div className={useStyles().paper}>
          {/* <Button
            type="submit"
            fullWidth
            variant="contained"
            color="primary"
            className={classes.submit}
          >
            Sign In
          </Button>
           */}
          <AppBar position="static"  style={{ background: 'rgba(0, 0, 0,0.95)' }} >
            <Toolbar>
              <Typography variant="h3" style={{color:'rgb(219, 191, 191)'}} >
                Pacify 
              </Typography>
            </Toolbar>
          </AppBar>
          {/* <div style={{ marginTop:'18%', marginBottom:'6%' ,width: '40%' }} >
            <Button variant="contained" size="large" style={{width: '100%',color:'red', backgroundColor:'white'}} href="Compiler">
              Compiler
            </Button>
          </div> */}
          <div style={{ marginTop:'8%', marginBottom:'6%' ,width: '40%' }} >
            <Link to="/real" style={{textDecoration: 'none'}} >
              <Button variant="contained" size="large" style={{width: '100%',color:'rgb(219, 191, 191)', backgroundColor:'rgba(0, 0, 0,0.95)',padding: '0px'}}>
                <h4>
                  Real Plagiarism
                </h4>
              </Button>
            </Link>  
          </div>
          <div style={{marginTop:'6%',  marginBottom:'1%', width: '40%' }}>
            <Link to="/online" style={{textDecoration: 'none'}} >
              <Button variant="contained" size="large" style={{width: '100%',color:'rgb(219, 191, 191)', backgroundColor:'rgba(0, 0, 0,0.95)',padding: '0px'}}>
                <h4>
                  Online Plagiarism
                </h4>
              </Button>
            </Link>
          </div>
          <div style={{marginTop:'6%', marginBottom:'1%', width: '40%'}}>
            <Link to="/semantic" style={{textDecoration: 'none'}}  >
            <Button variant="contained" size="large" style={{width: '100%',color:'rgb(219, 191, 191)', backgroundColor:'rgba(0, 0, 0,0.95)',padding: '0px'}}>
              <h4>
                Semantic Similarity
              </h4>
            </Button>
            </Link>
          </div>

          <div style={{marginTop:'6%', marginBottom:'1%', width: '40%'}}>
            <Link to="/entailment" style={{textDecoration: 'none'}}  >
            <Button variant="contained" size="large" style={{width: '100%',color:'rgb(219, 191, 191)', backgroundColor:'rgba(0, 0, 0,0.95)',padding: '0px'}}>
              <h4>
                Entailment Analysis
              </h4>
            </Button>
            </Link>
          </div>

          {/* <div></div> */}
          <div style={{alignSelf:'flex-end', justifyContent: 'flex-end', marginTop:'8%', marginBottom:'0%'}}>
            <h5 style={{color:'white'}}>
              by Aditya and Kartik
            </h5>
          </div>
        </div>
      </Grid>
      {/* <Grid item xs={false} sm={4} md={4} className={classes.image} /> */}
    </Grid>
)