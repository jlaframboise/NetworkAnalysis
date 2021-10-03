import * as React from 'react';
import { useTheme } from '@mui/material/styles';
import { Treemap, Pie, Line, XAxis, YAxis, Label, ResponsiveContainer } from 'recharts';
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

export default function TreeMapComponent() {
  const theme = useTheme();
  const [srcDist, setSrcDist] = useState([]);
  const [destDist, setDestDist] = useState([]);

  useEffect(() => {
    fetch('/src_freqs').then(res => res.json()).then(data => {
      const name_value_pairs = []
      data.dist.forEach(element => {
          name_value_pairs.push({
              "name": element[0],
              "value": element[1]
          })
      });
      setSrcDist(name_value_pairs);
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


  }, []);
  return (
    <React.Fragment>
      <Title>Source</Title>
      <ResponsiveContainer>
        <Treemap
          width={730}
          height={250}
          data={srcDist}
          dataKey="value"
          aspectRatio={5}
          stroke="#fff"
          fill="#8884d8"
        />
        
      </ResponsiveContainer>

      <Title>Destination</Title>
      <ResponsiveContainer>
        <Treemap
          width={730}
          height={250}
          data={destDist}
          dataKey="value"
          aspectRatio={5}
          stroke="#fff"
          fill="#8884d8"
        />
        
      </ResponsiveContainer>
    </React.Fragment>
  );
}