import * as React from 'react';
import { styled } from '@mui/material/styles';
import MuiDrawer from '@mui/material/Drawer';
import Toolbar from '@mui/material/Toolbar';
import List from '@mui/material/List';
import Divider from '@mui/material/Divider';
import IconButton from '@mui/material/IconButton';
import ChevronLeftIcon from '@mui/icons-material/ChevronLeft';
import ListItem from '@mui/material/ListItem';
import ListItemIcon from '@mui/material/ListItemIcon';
import ListItemText from '@mui/material/ListItemText';
import ListSubheader from '@mui/material/ListSubheader';
import DashboardIcon from '@mui/icons-material/Dashboard';
import ShoppingCartIcon from '@mui/icons-material/ShoppingCart';
import PeopleIcon from '@mui/icons-material/People';
import BarChartIcon from '@mui/icons-material/BarChart';
import LayersIcon from '@mui/icons-material/Layers';
import AssignmentIcon from '@mui/icons-material/Assignment';
import { useState, useEffect } from 'react';
import { Button } from '@mui/material';
import SimpleDialog from './SimpleDialog';


// apply styles to the MuiDrawer
const drawerWidth = 240;
const Drawer = styled(MuiDrawer, { shouldForwardProp: (prop) => prop !== 'open' })(
  ({ theme, open }) => ({
    '& .MuiDrawer-paper': {
      position: 'relative',
      whiteSpace: 'nowrap',
      width: drawerWidth,
      transition: theme.transitions.create('width', {
        easing: theme.transitions.easing.sharp,
        duration: theme.transitions.duration.enteringScreen,
      }),
      boxSizing: 'border-box',
      ...(!open && {
        overflowX: 'hidden',
        transition: theme.transitions.create('width', {
          easing: theme.transitions.easing.sharp,
          duration: theme.transitions.duration.leavingScreen,
        }),
        width: theme.spacing(7),
        [theme.breakpoints.up('sm')]: {
          width: theme.spacing(9),
        },
      }),
    },
  }),
);



/**
 * A function to make the drawer, and add in the 
 * upload pcap, add table, sniff packets, delete table
 * functionality
 * 
 * 
 * @param {updateDashboard} props 
 * @returns a functional component
 */
export default function MyDrawer(props) {

  const [tableNames, setTableNames] = useState([]);
  const [updateDrawer, setUpdateDrawer] = useState(0);
  // const [selectedValue, setSelectedValue] = useState(emails[1]);

  // fetch the table names to properly display them
  useEffect(() => {
    fetch('/get_table_names').then(res => res.json()).then(data => {
      const table_names_list = data.table_names.map((x) => { return x[0] })
      console.log(table_names_list)
      setTableNames(table_names_list);
    });


  }, [props.updateDashboard]);

  /**
   * A function to create a clickable table entry
   * for each table in the db. 
   */
  const savedTables = tableNames.map((table_name) => {
    return (
      <ListItem button onClick={() => {
        fetch('/set_current_table', {
          body: `table_name=${table_name}`,
          headers: {
            "Content-Type": "application/x-www-form-urlencoded",
          },
          method: 'post',

        }).then(res => res.json()).then(data => {
          console.log(data);
        });
        props.setUpdateDashboard(props.updateDashboard + 1);
      }}>
        <ListItemIcon>
          <AssignmentIcon />
        </ListItemIcon>
        <ListItemText primary={table_name} />
      </ListItem>
    )

  })

  /**
   * A function to upload and read a pcap file 
   * into the current table. 
   * 
   * 
   * @param {event} e 
   */
  const add_pcap_from_input_event = (e) => {

    const files = e.target.files
    const formData = new FormData()
    formData.append('file', files[0])

    fetch("/add_pcap", {
      method: "POST",
      body: formData
    }).then(res => res.json()).then(data => {
      console.log(data);
      props.setUpdateDashboard(props.updateDashboard + 1)
    }).catch(error => {
      console.error(error)
    });

  }

  /**
   * A function to sniff packets and then store those
   * packets in the current table. 
   * 
   * @param {event} e 
   */
  const sniff_packets_from_input_event = (e) => {

    fetch("/sniff", { method: 'POST' }).then(res => res.json()).then(data => {
      console.log(data);
      console.log("updating dashboard after sniff")
      props.setUpdateDashboard(props.updateDashboard + 1)
    }).catch(error => {
      console.error(error)
    });

  }

  /**
   * A function to delete the current table
   * by calling the api. 
   */
  const delete_current_table = () => {
    fetch("/delete_current_table", {
      method: "DELETE"
    }).then(res => res.json()).then(data => {
      console.log(data);
    }).catch(error => {
      console.error(error)
    });
  }


  return (
    <Drawer variant="permanent" open={props.open}>
      <Toolbar
        sx={{
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'flex-end',
          px: [1],
        }}
      >
        <IconButton onClick={props.toggleDrawer}>
          <ChevronLeftIcon />
        </IconButton>
      </Toolbar>
      <ListSubheader inset>Tables</ListSubheader>
      <List>{savedTables}</List>
      <ListSubheader inset>Operations</ListSubheader>
      <Button
        variant="contained"
        component="label"
      >
        Upload .pcap
        <input
          type="file"
          hidden
          onChange={(ev) => { console.log("triggered onSubmit from file upload. "); console.log(ev.target); add_pcap_from_input_event(ev) }}
        />
      </Button>
      <Divider />
      <Button
        variant="contained"
        component="label"
        onClick={e => { delete_current_table(); props.setUpdateDashboard(props.updateDashboard + 1) }}
      >
        Delete table
      </Button>
      <Divider />
      <Button
        variant="contained"
        component="label"
        onClick={e => { sniff_packets_from_input_event(e); }}
      >
        Sniff Packets
      </Button>

      <SimpleDialog updateDashboard={props.updateDashboard} setUpdateDashboard={props.setUpdateDashboard} />

    </Drawer>
  )
}



