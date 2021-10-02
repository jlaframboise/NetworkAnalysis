import * as React from 'react';
import { useTheme } from '@mui/material/styles';
import { PieChart, Pie, Line, XAxis, YAxis, Label, ResponsiveContainer } from 'recharts';
import Title from './Title';
import { useState, useEffect } from 'react';

// Generate Sales Data
function createData(time, amount) {
  return { time, amount };
}

const data01 = [
    {
      "name": "IP",
      "value": 400
    },
    {
      "name": "IPv6",
      "value": 50
    }
  ];
  const data02 = [
    {
      "name": "TCP",
      "value": 380
    },
    {
      "name": "UDP",
      "value": 70
    }
  ];

export default function PieChartComponent() {
  const theme = useTheme();
  const [transportLayerDist, setTransportLayerDist] = useState([]);
  const [inetLayerDist, setInetLayerDist] = useState([]);

  useEffect(() => {
    fetch('/transport_layer_freqs').then(res => res.json()).then(data => {
      const name_value_pairs = []
      data.transport_layer_dist.forEach(element => {
          name_value_pairs.push({
              "name": element[0],
              "value": element[1]
          })
      });
      setTransportLayerDist(name_value_pairs);
    });

    fetch('/inet_layer_freqs').then(res => res.json()).then(data => {
        const name_value_pairs = []
        data.inet_layer_dist.forEach(element => {
            name_value_pairs.push({
                "name": element[0],
                "value": element[1]
            })
        });
        setInetLayerDist(name_value_pairs);
      });


  }, []);
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