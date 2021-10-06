import * as React from 'react';
import { useTheme } from '@mui/material/styles';
import { PieChart, Pie, Line, XAxis, YAxis, Label, ResponsiveContainer } from 'recharts';
import Title from './Title';
import { useState, useEffect } from 'react';

/**
 * A functional component to render a pie chart which
 * will show the breakdown of packet types for the 
 * internet and transport layers.
 * 
 * @param {*} props 
 * @returns 
 */
export default function PieChartComponent(props) {
  const theme = useTheme();

  // use the value counts for source and destination ip
  const [transportLayerDist, setTransportLayerDist] = useState([]);
  const [inetLayerDist, setInetLayerDist] = useState([]);


  // fetch the value counts for source and dest ip
  useEffect(() => {
    fetch('/transport_layer_freqs').then(res => res.json()).then(data => {
      const name_value_pairs = []
      data.dist.forEach(element => {
        name_value_pairs.push({
          "name": element[0],
          "value": element[1]
        })
      });
      setTransportLayerDist(name_value_pairs);
    });

    fetch('/inet_layer_freqs').then(res => res.json()).then(data => {
      const name_value_pairs = []
      data.dist.forEach(element => {
        name_value_pairs.push({
          "name": element[0],
          "value": element[1]
        })
      });
      setInetLayerDist(name_value_pairs);
    });


  }, [props.updateDashboard]);

  // display the rechart.PieChart
  return (
    <React.Fragment>
      <Title>Today</Title>
      <ResponsiveContainer>
        <PieChart width={730} height={250}>
          <Pie data={inetLayerDist} dataKey="value" nameKey="name" cx="50%" cy="50%" outerRadius={50} fill="#8884d8" />
          <Pie data={transportLayerDist} dataKey="value" nameKey="name" cx="50%" cy="50%" innerRadius={60} outerRadius={80} fill="#82ca9d" label />
        </PieChart>
      </ResponsiveContainer>
    </React.Fragment>
  );
}