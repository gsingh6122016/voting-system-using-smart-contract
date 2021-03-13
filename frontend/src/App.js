import './App.css';
import { Switch, Route } from "react-router-dom";
import Candidates from './components/Candidates';
import Login from './components/Login';
import Results from './components/Results';

function App() {
  return (
    <>  
      <Switch>
      <Route exact path="/" component={Login} />
      <Route exact path="/candidates" component={Candidates} />
      <Route exact path="/results" component={Results} />
      </Switch>

    </>
  );
}

export default App;
