import * as React from 'react';
import { useEffect, useState } from 'react';
import Link from '@mui/material/Link';
import Typography from '@mui/material/Typography';
import Title from './Title';

function preventDefault(event) {
  event.preventDefault();
}

export default function PacketsCount(props) {

  const [packetCount, setPacketCount] = useState(0);
  const [tableName, setTableName] = useState("getting table name...");

  useEffect(() => {
    fetch('/count_packets').then(res => res.json()).then(data => {
      
      setPacketCount(data.packet_count);
    });

    fetch('/get_current_table_name').then(res => res.json()).then(data => {
      
      setTableName(data.table_name);
    });


  }, [props.updateDashboard]);


  return (
    <React.Fragment>
      <Title>Number of Packets</Title>
      <Typography component="p" variant="h4">
        {packetCount}
      </Typography>
      <Typography color="text.secondary" sx={{ flex: 1 }}>
        in {tableName} table
      </Typography>
      <div>
        <Link color="primary" href="#" onClick={preventDefault}>
          View balance
        </Link>
      </div>
    </React.Fragment>
  );
}
