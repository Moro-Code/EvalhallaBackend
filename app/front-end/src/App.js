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
    },
    {
      linkText: "Upload",
      link: "/upload",
      icon: "icon-upload"
    },
    {
      linkText: "Download",
      link: "/download",
      icon: "icon-download"
    }
  ]

  return (
    <div className="App">
      <NavMenu links = {routes}>   
      </NavMenu>
      <div className= "content">
        <Switch>
          <Route path = "/">
              <h1>Hello this is an extremely long h1 tag to test if something works</h1> 
          </Route>
        </Switch>
      </div>
    </div>
  );
}

export default App;
