import * as React from 'react';
import { useTheme } from '@mui/material/styles';
import { BarChart, Pie, Line, XAxis, YAxis, Label, ResponsiveContainer, CartesianGrid, Tooltip, Bar, Legend } from 'recharts';
import Title from './Title';
import { useState, useEffect } from 'react';


export default function MyBarChart(props) {
  const theme = useTheme();
  const [countryDist, setCountryDist] = useState([]);
  const [destDist, setDestDist] = useState([]);

  useEffect(() => {
    fetch('/country_freqs').then(res => res.json()).then(data => {
      const name_value_pairs = []
      data.dist.forEach(element => {
          name_value_pairs.push({
              "name": element[0],
              "value": element[1]
          })
      });
      setCountryDist(name_value_pairs);
    });

    fetch('/dest_freqs').then(res => res.json()).then(data => {
        const name_value_pairs = []
        data.dist.forEach(element => {
            name_value_pairs.push({
                "name": element[0],
                "value": element[1]
            })
        });
        setDestDist(name_value_pairs);
      });

  }, [props.updateDashboard]);


  return (
    <React.Fragment>
      <Title>Top Countries</Title>
      <ResponsiveContainer>
      <BarChart width={730} height={250} data={countryDist}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="name" />
        <YAxis />
        <Tooltip />
        <Legend />
        <Bar dataKey="value" name="Packet Count" fill="#8884d8" />
      </BarChart>
        
      </ResponsiveContainer>
    </React.Fragment>
  );
}