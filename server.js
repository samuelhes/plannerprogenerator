const express = require('express');
const cors = require('cors'); // If available
const fs = require('fs');
const path = require('path');
const xlsx = require('xlsx'); // If available, otherwise need another way

const app = express();
const PORT = 3000;

app.use(express.json());
app.use(cors());
app.use(express.static('public'));

// Load data
const customers = JSON.parse(fs.readFileSync(path.join(__dirname, 'data', 'clientes_ficticios.json'), 'utf-8'));
const csvTemplatePath = path.join(__dirname, 'data', 'plantilla_ordenes.csv');
const csvTemplate = fs.readFileSync(csvTemplatePath, 'utf-8');

// Parse headers
const headers = csvTemplate.split('\n')[0].split(';');

app.post('/api/generate', (req, res) => {
    const { count, city, country, itemsPerOrder, timeWindowStart, timeWindowEnd, deliveryDate } = req.body;

    // Filter customers
    let validCustomers = customers.filter(c =>
        (city && c.city.toLowerCase().includes(city.toLowerCase())) &&
        (country && c.country.toLowerCase().includes(country.toLowerCase()))
    );
    if (validCustomers.length === 0) validCustomers = customers; // Fallback

    const wb = xlsx.utils.book_new();
    const wsData = [headers]; // Header row

    for (let i = 0; i < count; i++) {
        const customer = validCustomers[i % validCustomers.length]; // Round robin or random
        // Generate Row Data based on headers
        // This is where we map specific columns.
        // For simplicity in this quick draft, we'd map "DIRECCION" -> customer.address, etc.

        // ... Logic to be completed ...
    }

    // ...
});

// app.listen ...
