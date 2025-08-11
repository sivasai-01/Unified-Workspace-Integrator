import { useState } from 'react';
import {
    Box,
    TextField,
    Button,
} from '@mui/material';
import axios from 'axios';

const endpointMapping = {
    'Notion': 'notion',
    'Airtable': 'airtable',
    'HubSpot': 'hubspot',
};

export const DataForm = ({ integrationType, credentials }) => {
    const [loadedData, setLoadedData] = useState(null);
    const [stretched, setStretched] = useState(false);
    const endpoint = endpointMapping[integrationType];

    const handleLoad = async () => {
        try {
            const formData = new FormData();
            formData.append('credentials', JSON.stringify(credentials));
            const response = await axios.post(`http://localhost:8000/integrations/${endpoint}/load`, formData);
            const data = response.data;
            console.log('Loaded data of', endpoint,': ',data);
            setLoadedData(data);
            setStretched(true);
        } catch (e) {
            alert(e?.response?.data?.detail);
        }
    };

    const handleClear = () => {
        setLoadedData(null);
        setStretched(false);
    };

    return (
        <Box display='flex' justifyContent='flex-start' alignItems='center' flexDirection='column' width='100vw' minHeight='100vh'>
            <Box
                display='flex'
                flexDirection='column'
                width={stretched ? '90vw' : '500px'}
                transition="width 0.3s"
                sx={{ mt: 0 }}
            >
                <TextField
                    label="Loaded Data"
                    value={
                        loadedData
                            ? JSON.stringify(loadedData, null, 4)
                            : ''
                    }
                    sx={{
                        mt: 0,
                        width: '100%',
                        fontFamily: 'monospace',
                        '& .MuiInputBase-input': {
                            fontFamily: 'monospace',
                            textAlign: 'left',
                            whiteSpace: 'pre',
                        },
                    }}
                    InputLabelProps={{ shrink: true }}
                    multiline
                    minRows={stretched ? 16 : 6}
                    disabled
                />
                <Button
                    onClick={handleLoad}
                    sx={{ mt: 2, width: '200px', alignSelf: 'center' }} // Reduced width, centered
                    variant='contained'
                >
                    Load Data
                </Button>
                <Button
                    onClick={handleClear}
                    sx={{ mt: 1, width: '200px', alignSelf: 'center' }} // Reduced width, centered
                    variant='contained'
                >
                    Clear Data
                </Button>
            </Box>
        </Box>
    );
}
