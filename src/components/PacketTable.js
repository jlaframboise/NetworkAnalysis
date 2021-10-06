import * as React from 'react';
import { useState, useEffect } from 'react';
import Link from '@mui/material/Link';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Title from './Title';


function preventDefault(event) {
  event.preventDefault();
}


/**
 * A functional component which displays a visual table of
 * a subset of the packets in the current table. 
 * 
 * @param {*} props 
 * @returns 
 */
export default function PacketTable(props) {


  // track the currently loaded packets
  const [currentPackets, setCurrentPackets] = useState([]);

  useEffect(() => {
    fetch('/packets?packet_limit=5').then(res => res.json()).then(data => {

      const newPackets = data.packets
      console.log(data.packets)
      setCurrentPackets(newPackets);
    });
  }, [props.updateDashboard]);


  // render the table
  return (
    <React.Fragment>
      <Title>Packets</Title>
      <Table size="small">
        <TableHead>
          <TableRow>
            <TableCell>Internet Layer</TableCell>
            <TableCell>Transport Layer</TableCell>
            <TableCell>Source</TableCell>
            <TableCell>Destination</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {/* for every packet, show key information */}
          {currentPackets.map((row) => (
            <TableRow key={row[0]}>
              <TableCell>{row[1]}</TableCell>
              <TableCell>{row[2]}</TableCell>
              <TableCell>{row[3]}</TableCell>
              <TableCell>{row[4]}</TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
      <Link color="primary" href="#" onClick={preventDefault} sx={{ mt: 3 }}>
        See more packets
      </Link>
    </React.Fragment>
  );
}
