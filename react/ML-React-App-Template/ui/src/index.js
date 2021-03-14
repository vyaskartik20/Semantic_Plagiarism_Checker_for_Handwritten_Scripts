// import React from 'react';
// import ReactDOM from 'react-dom';
// import './index.css';
// import App from './App';
// import Home from './App';
// import * as serviceWorker from './serviceWorker';

// ReactDOM.render(<Home />, document.getElementById('root'));

// // If you want your app to work offline and load faster, you can change
// // unregister() to register() below. Note this comes with some pitfalls.
// // Learn more about service workers: https://bit.ly/CRA-PWA
// serviceWorker.unregister();


import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import App from './App';
// import Home from './components/Home';
import * as serviceWorker from './serviceWorker';
// import Pomodoro from './componentsPomo/Pomodoro';
// import Notebook from './componentsNote/Notebook';
// import Compiler from './componentsCompiler/Compiler';
import RealPlagiarism from './realPlagiarism/realPlagiarism';
import OnlinePlagiarism from './onlinePlagiarism/onlinePlagiarism';
import SemanticSimilarity from './semanticSimilarity/semanticSimilarity';
import EntailmentAnalysis from './entailmentAnalysis/entailmentAnalysis';
// import {Router, Route, IndexRoute} from "react-router"
// import createHistory from 'history/createBrowserHistory'

ReactDOM.render(
  <React.StrictMode>
    <App />
    {/* <Router history={createHistory} >
      <Route path={"App"} component={App} />
    </Router> */}
  </React.StrictMode>,
  document.getElementById('root')
);

// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: https://bit.ly/CRA-PWA
serviceWorker.unregister();


// , browserHistory
// history={browserHistory}