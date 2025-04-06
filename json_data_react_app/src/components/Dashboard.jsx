import React, { useEffect } from "react";
import { Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Modal, Box, Button, Paper } from "@mui/material";
import axios from "axios";
import JSONEditor from "react-ace";
import "ace-builds/src-noconflict/mode-json";
import "ace-builds/src-noconflict/theme-monokai";
import { Link } from "react-router-dom";

import deleteIcon from "../assets/delete.png";
import { useState } from "react";


const Dashboard = ({ pdfData, setPdfData }) => {
    const NGROK_BASE_URL = "http://192.168.12.121:8005"; // Your current ngrok URL
    const [jsonData, setJsonData] = useState(null);
    const [openModal, setOpenModal] = useState(false);
    const [currentJsonType, setCurrentJsonType] = useState("");
    const [currentId, setCurrentId] = useState(null);
    const [loading, setLoading] = useState(false);

    const fetchPdfData = async () => {
        try {
            const response = await axios.get(`${NGROK_BASE_URL}/forms/api/get-all-pdfs/`, {
                headers: {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json',
                },
            });
            if (response.status === 200) {
                setPdfData(response.data);
            }
        } catch (error) {
            console.error("Error fetching PDF data:", error);
        }
    };

    useEffect(() => {
        fetchPdfData();
    }, []);

    const handleJsonClick = async (jsonPath, id, key) => {
        try {
            const response = await axios.get(jsonPath);
            setJsonData(response.data);
            setCurrentJsonType(key);
            setCurrentId(id);
            setOpenModal(true);
        } catch (error) {
            console.error("Error fetching JSON data:", error);
        }
    };

    const handleSubmitChanges = async () => {
        if (!currentId || !jsonData || !currentJsonType) return;
        try {
            const apiEndpoint = `${NGROK_BASE_URL}/forms/api/update/${currentId}/`;
            const updatedData = {
                [currentJsonType]: jsonData,
            };

            await axios.put(apiEndpoint, updatedData, {
                headers: {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json',
                },
            });

            alert("JSON data updated successfully");
            fetchPdfData();
            setOpenModal(false);
        } catch (error) {
            alert("Failed to update JSON data");
            console.error("Error updating JSON data:", error);
        }
    };
    const deleteRow = async (id) => {
        try {
            const apiEndpoint = `${NGROK_BASE_URL}/forms/pdf-processing/delete/${id}/`;


            await axios.delete(apiEndpoint, {
                headers: {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json',
                },
            });

            alert("row delete successfully");
            fetchPdfData();
        } catch (error) {

        }
    }
    const style = {
        position: 'absolute',
        top: '50%',
        left: '50%',
        transform: 'translate(-50%, -50%)',
        width: "80%",
        bgcolor: 'white',
        p: 1,
        height:"570px",
        overflow:"hidden",
        borderRadius:2
      };
    return (
        <Box>
            <Box py={2} sx={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
                <Button variant="contained" color="success" component={Link} to="/upload">
                    Upload PDF
                </Button>
                {/* <a href="http://192.168.12.121:8005/users/login/">
                    <Button variant="contained" color="success">
                        Visit Dashbaord Site
                    </Button>
                </a> */}
            </Box>
            <TableContainer component={Paper}>
                <Table>
                    <TableHead>
                        <TableRow>
                            <TableCell>Delete</TableCell>
                            <TableCell>Input PDF</TableCell>
                            <TableCell>Processed PDF</TableCell>
                            <TableCell>Form Data JSON</TableCell>
                            <TableCell>Normalized Data JSON</TableCell>
                            <TableCell>Uploaded At</TableCell>
                        </TableRow>
                    </TableHead>
                    <TableBody>
                        {pdfData?.map((item) => (
                            <TableRow key={item.id} >
                                <TableCell onClick={() => deleteRow(item?.id)}><img src={deleteIcon} style={{ height: "20px", width: "20px", cursor: "pointer" }} /></TableCell>
                                <TableCell>
                                    <a
                                        href={`${NGROK_BASE_URL}${item.input_pdf}`}
                                        target="_blank"
                                        rel="noopener noreferrer"
                                    >
                                        {item.input_pdf}
                                    </a>
                                </TableCell>
                                <TableCell>
                                    <a
                                        href={`${NGROK_BASE_URL}${item.processed_pdf}`}
                                        target="_blank"
                                        rel="noopener noreferrer"
                                    >
                                        {item.processed_pdf}
                                    </a>
                                </TableCell>
                                <TableCell>
                                    <Button
                                        variant="outlined"
                                        onClick={() =>
                                            handleJsonClick(`${NGROK_BASE_URL}${item.form_data_json}`, item?.id, "form_data_json")
                                        }
                                    >
                                        {item.form_data_json}
                                    </Button>
                                </TableCell>
                                <TableCell>
                                    <Button
                                        variant="outlined"
                                        onClick={() =>
                                            handleJsonClick(`${NGROK_BASE_URL}${item.normalized_data_json}`, item?.id, "normalized_data_json")
                                        }
                                    >
                                        {item.normalized_data_json}
                                    </Button>
                                </TableCell>
                                <TableCell>{item.uploaded_at}</TableCell>
                            </TableRow>
                        ))}
                    </TableBody>
                </Table>
            </TableContainer>
            <Modal open={openModal} onClose={() => setOpenModal(false)}>
                <Box
                sx={style}
                    // sx={{
                    //     padding: 2,
                    //     backgroundColor: "white",
                    //     width: "90%",
                    //     height:"100",
                    //     margin: "auto",
                    //     marginTop: "1%",
                    //     overflowY: "auto",
                    // }}
                >
                    <JSONEditor
                        mode="json"
                        theme="monokai"
                        value={JSON.stringify(jsonData, null, 2)} // Display JSON in editor
                        onChange={(value) => {
                            try {
                                // Parse the updated JSON from the editor
                                const updatedJson = JSON.parse(value);
                                setJsonData(updatedJson); // Update the state with the parsed JSON
                            } catch (error) {
                                // Optionally log the error or show a message to the user
                                console.error("Invalid JSON input:", error);
                            }
                        }}
                        width="100%" // Ensure the editor spans full width
                        // height="700px" // Fixed height for the editor
                    />

                    <Box sx={{ display: 'flex', flexDirection: { xs: 'column', sm: 'row' }, gap: 2, marginTop: 2 }}>
                        <Button variant="contained" onClick={() => setOpenModal(false)} sx={{ flex: 1 }}>
                            Close
                        </Button>
                        <Button variant="contained" onClick={handleSubmitChanges} sx={{ flex: 1 }}>
                            Save Changes
                        </Button>
                    </Box>
                </Box>
            </Modal>
        </Box>
    );
};

export default Dashboard;
