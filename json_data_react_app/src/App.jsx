import React, { useState } from "react";
import { BrowserRouter as Router, Route, Routes, Link } from "react-router-dom";
import { Container, Button, CssBaseline, Typography, Box } from "@mui/material";
import Dashboard from "./components/Dashboard";
import UploadForm from "./components/UploadForm";

function App() {
  const [pdfData, setPdfData] = useState([]);



  return (
    <Box p={4}>

      <Router>
        <CssBaseline />
        {/* <Container> */}
        <Typography variant="h2" align="center" color="primary" gutterBottom>
          PDF Dashboard
        </Typography>
        <Routes>
          <Route
            path="/"
            element={<Dashboard pdfData={pdfData} setPdfData={setPdfData} />}
          />
          <Route path="/upload" element={<UploadForm setPdfData={setPdfData} />} />
        </Routes>
        {/* </Container> */}
      </Router>
    </Box>

  );
}

export default App;
