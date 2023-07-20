document.addEventListener('DOMContentLoaded', function() {
  updateLineGraph("SaltLake")
})



function updateLineGraph(buttonId) {
  // Remove active class from all buttons
  document.querySelectorAll('.tab-group button').forEach(btn => btn.classList.remove('active'));

  // Add active class to the clicked button
 
  const button = document.getElementById(buttonId);
  button.classList.add('active');
 
  // Update line graph data based on countyType
  const data = getDataByCounty(buttonId);

  // Clear existing line graph
  d3.select('#d3-interactive').html('');

  // Draw line graph with updated data
  drawLineGraph(data);
}


function getDataByCounty(buttonId) {
  // Return the appropriate data based on countyType
  // You can customize this function to fetch data from an API or use predefined data
  if (buttonId === 'SaltLake') {
    d3.csv("static/Utah, Salt Lake.csv").then(data=>{
      drawLineGraph(data)})
  } else if (buttonId === 'Hillsborough') {
    d3.csv("static/Florida, Hillsborough.csv").then(data=>{
      drawLineGraph(data)})
  }else if (buttonId === 'Multnomah') {
    d3.csv("static/Oregon, Multnomah.csv").then(data=>{
      drawLineGraph(data)})
  }else if (buttonId === 'Brunswick') {
    d3.csv("static/Virginia, Brunswick.csv").then(data=>{
      drawLineGraph(data)})
  }else if (buttonId === 'Yancey') {
    d3.csv("static/North Carolina, Yancey.csv").then(data=>{
      drawLineGraph(data)})
  }else if (buttonId === 'Ogemaw') {
    d3.csv("static/Michigan, Ogemaw.csv").then(data=>{
      drawLineGraph(data)})
  }
}

function drawLineGraph(data) {
  console.log(data)
  // Set up the dimensions and margins of the plot
  const width = 800;
  const height = 600;
  const margin = { top: 20, right: 20, bottom: 30, left: 40 };

  // Create the SVG element
  const svg = d3.select('#d3-interactive')
    .attr('width', width + margin.left + margin.right)
    .attr('height', height + margin.top + margin.bottom)
    .append('g')
    .attr('transform', `translate(${margin.left}, ${margin.top})`);

  // Create scales for the x and y axes
  const parseDate = d3.timeParse('%Y-%m-%d');
    data.forEach(d => d.Date = parseDate(d.Date));

    // Create scales for the x and y axes
    const xScale = d3.scaleTime()
      .domain(d3.extent(data, d => d.Date))
      .range([0, width]);

    const yScale = d3.scaleLinear()
      .domain([0, d3.max(data, d => Math.max(d.Predicted_Cases, d.Cases))])
      .range([height, 0]);

    // Create x-axis
    const xAxis = d3.axisBottom(xScale);
    svg.append('g')
      .attr('transform', `translate(0, ${height})`)
      .call(xAxis);

    // Create y-axis
    const yAxis = d3.axisLeft(yScale);
    svg.append('g')
      .call(yAxis);


    const legendItems = [
      { label: 'Predicted Cases', color: 'red' },
      { label: 'Actual Cases', color: 'blue' },
      // You can add more legend items for additional lines if needed
  ];

  const legendGroup = svg.append('g')
      .attr('class', 'legend')
      .attr('transform', `translate(${width - 700}, 20)`);

  const legendEntries = legendGroup.selectAll('.legend-entry')
      .data(legendItems)
      .enter()
      .append('g')
      .attr('class', 'legend-entry')
      .attr('transform', (d, i) => `translate(0, ${i * 20})`);

  legendEntries.append('rect')
      .attr('width', 10)
      .attr('height', 10)
      .attr('fill', d => d.color);

  legendEntries.append('text')
      .attr('x', 15)
      .attr('y', 10)
      .text(d => d.label);

// Create a line generator
const predictedLine = d3.line()
    .x(d => xScale(d.Date))
    .y(d => yScale(d.Predicted_Cases));

  // Create the line path for the predicted cases
  svg.append('path')
    .datum(data)
    .attr('class', 'line predicted')
    .attr('d', predictedLine)
    .attr('fill', 'none') // Remove any fill
    .attr('stroke', 'red') // Customize the color for the actual cases;

  // Create a line generator for the actual cases
  const actualLine = d3.line()
    .x(d => xScale(d.Date))
    .y(d => yScale(d.Cases));

    // Create the line path for the actual cases
    svg.append('path')
      .datum(data)
      .attr('class', 'line actual')
      .attr('d', actualLine)
      .attr('fill', 'none') // Remove any fill
      .attr('stroke', 'blue') // Customize the color for the actual cases;
}
