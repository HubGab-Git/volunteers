<!DOCTYPE html>
<html>
  <head>
    <title>Sample Website</title>
    <link rel="stylesheet" href="styles.css">
    <style>
      table {
        width: 100%;
        border-collapse: collapse;
      }
      table, th, td {
        border: 1px solid black;
      }
      th, td {
        padding: 8px;
        text-align: left;
      }
      th {
        background-color: #f2f2f2;
      }
    </style>
  </head>
  <body>
    <h1>Welcome to the Sample Website</h1>
    <table id="data-table">
      <thead>
        <tr>
          <th>Name</th>
          <th>Email</th>
          <th>State</th>
          <th>Region</th>
          <th>City</th>
          <th>Admin of State</th>
          <th>Admin of Region</th>
          <th>Admin of City</th>
          <th>Superadmin</th>
          <th>Phone Number</th>
        </tr>
      </thead>
      <tbody id="table-body">
        <!-- Dynamic rows will be appended here -->
      </tbody>
    </table>
    <script>
      // Fetch data from the API Gateway
      async function fetchDataFromApiGateway() {
        const apiUrl = "${api_gateway_url}";
        try {
          const response = await fetch(apiUrl);
          if (!response.ok) {
            throw new Error('HTTP error ' + response.status);
          }
          const data = await response.json();
          return data;
        } catch (error) {
          console.error('Error fetching data:', error);
          throw error;
        }
      }

      // Call the fetchDataFromApiGateway function and update the table content
      fetchDataFromApiGateway()
        .then(data => {
          const tableBody = document.getElementById('table-body');
          data.forEach(row => {
            const tr = document.createElement('tr');
            Object.keys(row).forEach(key => {
              const td = document.createElement('td');
              td.textContent = row[key];
              tr.appendChild(td);
            });
            tableBody.appendChild(tr);
          });
        })
        .catch(error => {
          console.error('Error updating table content:', error);
        });
    </script>
  </body>
</html>
