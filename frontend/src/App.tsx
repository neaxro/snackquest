import { BrowserRouter, Routes, Route } from "react-router-dom";
import MainLayout from "./layouts/MainLayout";
import HomePage from "./pages/HomePage";
import CalculatorPage from "./pages/CalculatorPage";
import MachinesPage from "./pages/MachinesPage";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route element={<MainLayout />}>
          <Route path="/" element={<HomePage />} />
          <Route path="/calculator" element={<CalculatorPage />} />
          <Route path="/machines" element={<MachinesPage />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;
