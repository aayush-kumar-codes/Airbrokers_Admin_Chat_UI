import axios from "axios";

export const fetchPdfData = async (url) => {
    try {
        const response = await axios.get(url);
        return response.data;
    } catch (error) {
        console.error("Error fetching PDF data", error);
        throw error;
    }
};
