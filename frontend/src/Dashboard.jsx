import React, { useState } from 'react';
import styles from './Dashboard.module.css'; // Import the CSS Module
import axios from 'axios';

function Dashboard() {
    const [tableData, setTableData] = useState([]);
    const [milkingCapacity, setMilkingCapacity] = useState(0);
    const [isDropdownVisible, setIsDropdownVisible] = useState(false);

    // Handle input change for milking capacity
    const handleCapacityChange = (event) => {
        setMilkingCapacity(event.target.value);
    };

    // Generate rows based on milking capacity
    const generateRows = () => {
        const rows = Array.from({ length: milkingCapacity }, () => ({
            cowId: '',
            milkYield: '',
            timeSinceLastMilk: '',
            dailyFeedQuantity: '',
            enclosureTemp: '',
            outsideTemp: '',
            feedType: '',
            bovineAge: '',
            health: '',
            lactationStage: '',
            breed: '',
            country: ''
        }));
        setTableData(rows);
    };

    // Add a new row
    const addRow = () => {
        setTableData([
            ...tableData,
            {
                cowId: '',
                milkYield: '',
                timeSinceLastMilk: '',
                dailyFeedQuantity: '',
                enclosureTemp: '',
                outsideTemp: '',
                feedType: '',
                bovineAge: '',
                health: '',
                lactationStage: '',
                breed: '',
                country: ''
            }
        ]);
    };

    // Delete a specific row
    const deleteRow = (index) => {
        setTableData((prevData) => prevData.filter((_, i) => i !== index));
    };

    // Sort the table based on a column index
    const sortTable = (columnIndex) => {
        const sortedData = [...tableData].sort((a, b) => {
            const aValue = Object.values(a)[columnIndex];
            const bValue = Object.values(b)[columnIndex];
            return aValue > bValue ? 1 : aValue < bValue ? -1 : 0;
        });
        setTableData(sortedData);
    };

    // Handle file upload
    const handleFileUpload = (event) => {
        const file = event.target.files[0];
        if (file) {
            console.log('File uploaded:', file);
            // Add file upload logic here if needed
        }
    };

    // Toggle dropdown visibility
    const toggleDropdown = () => {
        setIsDropdownVisible(!isDropdownVisible);
    };

    // Handle clicks outside the dropdown
    React.useEffect(() => {
        const handleClickOutside = (event) => {
            if (!event.target.matches(`.${styles.dropbtn}`)) {
                setIsDropdownVisible(false);
            }
        };
        window.addEventListener('click', handleClickOutside);
        return () => {
            window.removeEventListener('click', handleClickOutside);
        };
    }, []);

    const handleSubmit = async () => {
        try {
            const response = await axios.post('http://localhost:5000/api/submit', tableData, {
                headers: {
                    'Content-Type': 'application/json',
                },
            });
            console.log(response.data);
            alert('Data submitted successfully!');
        } catch (error) {
            console.error('Error submitting data:', error);
            alert('Error submitting data');
        }
    };
    
    return (
        <div>
            {/* Header Section */}
            <div className={styles.container}>
                <h1 className={styles.header}>Cowlibrate Solutions</h1>
                <p>Helping farmers and cattlemen to maximize dairy production and scheduling</p>
            </div>

            {/* Dropdown Menu */}
            <div className={styles.dropdown}>
                <button className={styles.dropbtn} onClick={toggleDropdown}>
                    Dropdown
                </button>
                {isDropdownVisible && (
                    <div className={styles.dropdownContent}>
                        <a href="/homescreen">Homescreen</a>
                        <a href="/insights">Insights</a>
                        <a href="/schedules">Schedules</a>
                    </div>
                )}
            </div>

            <hr />

            <div className={styles.milkingParlorContainer}>
                <label htmlFor="milking-capacity-input" className={styles.milkingCapacityLabel}>Milking Parlor Capacity</label>
                <input
                    type="number"
                    id="milking-capacity-input"
                    name="capacity_number"
                    value={milkingCapacity}
                    onChange={handleCapacityChange}
                    className={styles.milkingCapacityInput}
                    required
                />
                <button type="button" className={styles.button} onClick={generateRows}>
                    Generate Rows
                </button>
            </div>

            {/* File Upload */}
            <div className={styles.uploadContainer}>
                <form id="upload-form" method="POST" encType="multipart/form-data" action="/upload">
                    <input type="file" name="file" onChange={handleFileUpload} className={styles.fileInput} />
                </form>
            </div>

            <hr />

            {/* Table Section */}
            <div className={styles.tableContainer}>
                <table>
                    <thead>
                        <tr>
                            {[
                                'Cow ID',
                                'Milk Yield (Gallons)',
                                'Time since last Milk',
                                'Daily Feed Quantity',
                                'Enclosure Temperature (°C)',
                                'Outside Temperature (°C)',
                                'Feed type',
                                'Bovine Age',
                                'Health',
                                'Lactation Stage',
                                'Breed of Bovine',
                                'Country'
                            ].map((header, index) => (
                                <th key={index} onClick={() => sortTable(index)}>
                                    {header}
                                </th>
                            ))}
                        </tr>
                    </thead>
                    <tbody>
                        {tableData.map((row, rowIndex) => (
                            <tr key={rowIndex}>
                                {Object.values(row).map((value, colIndex) => (
                                    <td key={colIndex}>
                                        <input
                                            type="text"
                                            value={value}
                                            onChange={(e) => {
                                                const updatedData = [...tableData];
                                                const key = Object.keys(row)[colIndex];
                                                updatedData[rowIndex][key] = e.target.value;
                                                setTableData(updatedData);
                                            }}
                                        />
                                    </td>
                                ))}
                            </tr>
                        ))}
                    </tbody>
                </table>

                {/* Button Container for Add Row, Delete Row, and Submit */}
                <div className={styles.buttonContainer}>
                    {/* Add Row Button */}
                    <button className={styles.button} onClick={addRow}>
                        Add Row
                    </button>

                    {/* Delete Row Button */}
                    <button className={styles.button} onClick={() => deleteRow(tableData.length - 1)}>
                        Delete Row
                    </button>

                    {/* Submit Button */}
                    <button className={styles.button} onClick={handleSubmit}>
                        Submit
                    </button>
                </div>
            </div>
        </div>
    );
}

export default Dashboard;
