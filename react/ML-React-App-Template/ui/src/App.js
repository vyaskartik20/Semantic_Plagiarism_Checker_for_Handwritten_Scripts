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
import DevelopersInfo from './developersInfo/developersInfo';
import Background from './images/3.jfif';


const useStyles = makeStyles((theme) => ({
  
  root: {
    backgroundImage: `url(${Background})`,
    // backgroundRepeat: 'no-repeat',
    backgroundColor:
      theme.palette.type === 'light' ? theme.palette.grey[50] : theme.palette.grey[900],
      backgroundPosition: 'center',
    backgroundSize: 'cover',
    // height : '100%',
    width : '100%',
    // backgroundAttachment : 'fixed'
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
    height : '100%',
    textAlign: 'center'
    // backgroundColor:'black'
  },
  other: {
    // backgroundColor:'rgb(36,2,11)',
    // backgroundImage: require('./coding.jpg')
    // <img src={'./coding.jpg'} />
    // color:'white'
    // backgroundImage: `url(${Background})`,
    backgroundRepeat: 'no-repeat',
    backgroundColor: 'rgba(90, 56, 200, 0.5)',
      backgroundPosition: 'center',
    // backgroundSize: 'cover',
    alignContent : 'center',
    alignItems : 'center',
    textAlign : 'center',
    height : '90%'
  },
  otherMain: {
    // backgroundColor:'rgb(36,2,11)',
    // backgroundImage: require('./coding.jpg')
    // <img src={'./coding.jpg'} />
    // color:'white'
    backgroundImage: `url(${Background})`,
    backgroundRepeat: 'no-repeat',
    // backgroundColor:
    //   theme.palette.type === 'light' ? theme.palette.grey[50] : theme.palette.grey[900],
      backgroundPosition: 'center',
    backgroundSize: 'cover',
    height : '100%',
    width : '100%',
    backgroundAttachment : 'fixed'

    // marginTop : '5%'
  },
  options : {
    // backgroundColor: 'rgba(99, 160, 1, 0.767)',
    marginTop : '5%',
    // alignContent : 'center',
    height : '100%'
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
          <Route path="/developers" component={DevelopersInfo} />

          <Route path="/" component={Home} />
        </Switch>
      </div>
    </Router>
    
  );
}
  
  
const Home =() => (
  <Grid container component="main" className={useStyles().root}>
  {/* <CssBaseline /> */}
      {/* <Grid item xs={false} sm={4} md={1} className={useStyles().image} /> */}
      <Grid item xs={12} sm={8} md={12} className={useStyles().otherMain}component={Paper} elevation={6} square>
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
          <AppBar position="static"  style={{ background: 'rgba(90, 56, 200, 0.4)' , textAlign : 'center', justifyContent : 'center' }} >
            <Toolbar>
              <Typography variant="h3" style={{color:'rgba(255, 255, 255, 0.95)', width : '100%', textShadow : '1npx 1px rgb(100, 10, 255)'}} >
                Plagiarism, Similarity and Entailment Analysis
              </Typography>
            </Toolbar>
          </AppBar>

          <Grid container component="main" className = {useStyles().options}>
            <Grid item xs={12} sm={8} md={6} className={useStyles().other}component={Paper} elevation={6} square>
              <div style={{ marginTop:'8%', marginBottom:'6%' ,width: '100%', alignSelf : 'center', height : '40%'  }} >
                <Link to="/real" style={{textDecoration: 'none'}} >
                  <Button variant="contained" size="large" style={{width: '40%', height: '60px', color:'rgb(219, 191, 191)', backgroundColor:'rgba(100, 10, 255,0.65)',padding: '1px', justifyContent : 'center'}}>
                    <h5>
                      Real Plagiarism
                    </h5>
                  </Button>
                </Link>  
              </div>
              <div style={{marginTop:'6%',  marginBottom:'8%', width: '100%' }}>
                <Link to="/online" style={{textDecoration: 'none'}} >
                  <Button variant="contained" size="large" style={{width: '40%', height: '60px',color:'rgb(219, 191, 191)', backgroundColor:'rgba(100, 10, 255,0.65)',padding: '1px', justifyContent : 'center'}}>
                    <h5>
                      Online Plagiarism
                    </h5>
                  </Button>
                </Link>
              </div>
            </Grid>
            <Grid item xs={12} sm={8} md={6} className={useStyles().other} component={Paper} elevation={6} square>
              <div style={{marginTop:'8%', marginBottom:'6%', width: '100%'}}>
                <Link to="/semantic" style={{textDecoration: 'none'}}  >
                <Button variant="contained" size="large" style={{width: '40%', height: '60px',color:'rgb(219, 191, 191)', backgroundColor:'rgba(100, 10, 255,0.65)',padding: '1px', justifyContent : 'center'}}>
                  <h5>
                    Semantic Similarity
                  </h5>
                </Button>
                </Link>
              </div>

              <div style={{marginTop:'6%', marginBottom:'8%', width: '100%'}}>
                <Link to="/entailment" style={{textDecoration: 'none'}}  >
                <Button variant="contained" size="large" style={{width: '40%', height: '60px',color:'rgb(219, 191, 191)', backgroundColor:'rgba(100, 10, 255,0.65)',padding: '1px', justifyContent : 'center'}}>
                  <h5>
                    Entailment Analysis
                  </h5>
                </Button>
                </Link>
              </div>
            </Grid>
          </Grid>

            <div style={{alignSelf:'flex-end', justifyContent: 'flex-end', marginTop:'8%', marginBottom:'0%'}}>
              <Link to="/developers" style={{textDecoration: 'none'}}  >
                <Button variant="contained" size="large" style={{width: '100%', height: '30px', color:'rgba(219, 191, 191,0)', backgroundColor:'rgba(100, 10, 255,0)',padding: '1px', justifyContent : 'center'}}>
                  <h6 style={{color:'white'}}>
                    <em>
                      See Developer Info
                    </em>
                  </h6>
                </Button>
              </Link>
            </div>
        </div>
      </Grid>
      {/* <Grid item xs={false} sm={4} md={1} className={useStyles().image} /> */}
    </Grid>
)