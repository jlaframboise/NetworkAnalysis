import * as React from 'react';
import { useTheme } from '@mui/material/styles';
import { Treemap, Pie, Line, XAxis, YAxis, Label, ResponsiveContainer } from 'recharts';
import Title from './Title';
import { useState, useEffect } from 'react';


/**
 * A functional component to show a TreeMap
 * for the most common IP addresses that are
 * a source and are a destination. 
 * 
 * @param {*} props 
 * @returns 
 */
export default function TreeMapComponent(props) {
  const theme = useTheme();

  // keep track of the value counts for source and destination ips
  const [srcDist, setSrcDist] = useState([]);
  const [destDist, setDestDist] = useState([]);

  // fetch the value counts for the source and dest ips
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

  }, [props.updateDashboard]);


  // render the components
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