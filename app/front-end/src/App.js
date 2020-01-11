import React from 'react';
import NavMenu from "./components/organisms/navigation/navMenu"
import {
  Switch,
  Route
} from "react-router-dom"

function App() {
  const routes = [
    {
      linkText: "Home",
      link: "/",
      icon: "icon-survey-list"
    }
  ]

  return (
    <div className="App">
      <NavMenu links = {routes}>   
      </NavMenu>

      <Switch>
        <Route path = "/">
           <h1>Hello</h1> 
        </Route>
      </Switch>
    </div>
  );
}

export default App;
