import {createBrowserRouter} from "react-router-dom";
import Main from "../Layout/Main";
import Home from "../Pages/Home/Home";





import AiQuestion from "../Pages/Home/AiQuestion";
import Feedback from "../Pages/Home/Feedback";
import SurveyResult from "../Pages/Home/SurveyResult";


  

export const router = createBrowserRouter([
    {
      path: "/",
      element: <Main />,
        children: [
          {path: '/', element: <Home/>},
          // {path: '/start_survey', element: <StartSurvey/>},
          {path: '/ai_question', element: <AiQuestion/>},
          {path: '/feedback', element: <Feedback/>},
          {path: '/survey_result', element: <SurveyResult/>},
          
      ]
    },

    
    
  ]);