import React, { useState } from "react";
import { Button, TextField, Container, Typography, Box, Grid } from "@mui/material";
import axios from "axios";
import { useNavigate } from "react-router-dom";

const UploadForm = ({ setPdfData }) => {
    const navigate = useNavigate();
    const [file, setFile] = useState(null);
    const [loading, setLoading] = useState(false);

    const NGROK_BASE_URL = "http://192.168.12.121:8005";

    const handleFileChange = (e) => {
        setFile(e.target.files[0]);
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (!file) {
            alert("Please select a file before saving.");
            return;
        }

        const formData = new FormData();
        formData.append("file", file);

        try {
            setLoading(true)
            const response = await axios.post(`${NGROK_BASE_URL}/forms/api/process-pdf/`, formData);
            if (response.data.status === "success") {
                alert("PDF Uploaded Successfully!");
                setPdfData((prevData) => [...prevData, response.data]);
                navigate("/")
                setLoading(false)
            } else {
                alert("Error uploading PDF");
                setLoading(false)
            }
        } catch (err) {
            alert("API Error: " + err);
            setLoading(false)
        }
    };

    return (
        <Box
            sx={{
                display: "flex",
                justifyContent: "center",
                alignItems: "center",
                height: "100vh",
                backgroundColor: "#f4f6f8",
                padding: 2,
                width: "100%"
            }}
        >
            <Container maxWidth="sm" sx={{ backgroundColor: "white", padding: 4, borderRadius: 2, boxShadow: 3 }}>
                <Typography variant="h4" align="center" color="primary" gutterBottom sx={{ fontWeight: 600 }}>
                    Add PDF Upload
                </Typography>
                <form onSubmit={handleSubmit}>
                    <Grid container spacing={2} direction="column">
                        <Grid item>
                            <TextField
                                type="file"
                                fullWidth
                                variant="outlined"
                                onChange={handleFileChange}
                                inputProps={{ accept: "application/pdf" }}
                                sx={{
                                    borderRadius: "8px",
                                    backgroundColor: "#f5f5f5",
                                    padding: "8px 16px",
                                    "& .MuiOutlinedInput-root": {
                                        borderRadius: "8px"
                                    }
                                }}
                            />
                        </Grid>

                        <Grid item>
                            <Box sx={{ marginBottom: 2 }}>
                                <Typography variant="body1" sx={{ fontWeight: 500 }}>
                                    Processed PDF:
                                </Typography>
                                <Typography variant="body1" sx={{ fontWeight: 500 }}>
                                    Form Data JSON:
                                </Typography>
                                <Typography variant="body1" sx={{ fontWeight: 500 }}>
                                    Normalized Data JSON:
                                </Typography>
                                <Typography variant="body1" sx={{ fontWeight: 500 }}>
                                    Uploaded At:
                                </Typography>
                            </Box>
                        </Grid>

                        <Grid item>
                            <Button
                                variant="contained"
                                color="primary"
                                type="submit"
                                fullWidth
                                sx={{
                                    borderRadius: "8px",
                                    padding: "12px 0",
                                    fontSize: "16px",
                                    "&:hover": {
                                        backgroundColor: "#3f51b5"
                                    }
                                }}
                            >
                                {loading ? "Parsing the Pdf....." : "Save"}
                            </Button>
                        </Grid>
                    </Grid>
                </form>
            </Container>
        </Box>
    );
};

export default UploadForm;
