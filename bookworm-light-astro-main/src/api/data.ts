

const fetchApiData = async (apiUrl: string): Promise<any> => {
    try {
        const response = await fetch(apiUrl);
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error fetching API:', error);
        return null;
    }
};

export default fetchApiData;