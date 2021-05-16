import './App.css';
import { Switch, Route } from "react-router-dom";
import Candidates from './components/Candidates';
import Login from './components/Login';
import Results from './components/Results';
import Voted from './components/Voted';
import Admin from './components/Admin';
import AdminDashboard from './components/AdminDashboard';

function App() {
  return (
    <>  
      <Switch>
      <Route exact path="/" component={Login} />
      <Route exact path="/candidates" component={Candidates} />
      <Route exact path="/results" component={Results} />
      <Route exact path="/voted" component={Voted} />
      <Route exact path="/admin" component={Admin} />
      <Route exact path="/admin-dashboard" component={AdminDashboard} />
      </Switch>

    </>
  );
}

export default App;
