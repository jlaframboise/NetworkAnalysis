import * as React from 'react';
import { styled, createTheme, ThemeProvider } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import MuiDrawer from '@mui/material/Drawer';
import Toolbar from '@mui/material/Toolbar';
import List from '@mui/material/List';
import Typography from '@mui/material/Typography';
import Divider from '@mui/material/Divider';
import IconButton from '@mui/material/IconButton';
import Badge from '@mui/material/Badge';
import Container from '@mui/material/Container';
import Grid from '@mui/material/Grid';
import Paper from '@mui/material/Paper';
import Link from '@mui/material/Link';
import MenuIcon from '@mui/icons-material/Menu';
import ChevronLeftIcon from '@mui/icons-material/ChevronLeft';
import NotificationsIcon from '@mui/icons-material/Notifications';
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


export default function MyDrawer(props){

    const [tableNames, setTableNames] = useState([]);

    useEffect(() => {
        fetch('/get_table_names').then(res => res.json()).then(data => {
        const table_names_list = data.table_names.map((x)=>{return x[0]})
        console.log(table_names_list)
        setTableNames(table_names_list);
        });


    }, []);

    const mainListItems = (
        <div>
          <ListItem button>
            <ListItemIcon>
              <DashboardIcon />
            </ListItemIcon>
            <ListItemText primary="Dashboard" />
          </ListItem>
          <ListItem button>
            <ListItemIcon>
              <ShoppingCartIcon />
            </ListItemIcon>
            <ListItemText primary="Orders" />
          </ListItem>
          <ListItem button>
            <ListItemIcon>
              <PeopleIcon />
            </ListItemIcon>
            <ListItemText primary="Customers" />
          </ListItem>
          <ListItem button>
            <ListItemIcon>
              <BarChartIcon />
            </ListItemIcon>
            <ListItemText primary="Reports" />
          </ListItem>
          <ListItem button>
            <ListItemIcon>
              <LayersIcon />
            </ListItemIcon>
            <ListItemText primary="Integrations" />
            
          </ListItem>
        </div>
      );

    const secondaryListItems = (
        <div>
          <ListSubheader inset>Saved reports</ListSubheader>
          <ListItem button onClick={()=>{console.log("Wow you clicked current month!")}}>
            <ListItemIcon>
              <AssignmentIcon />
            </ListItemIcon>
            <ListItemText primary="Current month" />
          </ListItem>
          <ListItem button>
            <ListItemIcon>
              <AssignmentIcon />
            </ListItemIcon>
            <ListItemText primary="Last quarter" />
          </ListItem>
          <ListItem button>
            <ListItemIcon>
              <AssignmentIcon />
            </ListItemIcon>
            <ListItemText primary="Year-end sale" />
          </ListItem>
        </div>
      );



      const savedTables = tableNames.map((table_name)=>{
          return (
            <ListItem button onClick={()=>{
                fetch('/set_current_table',{
                    body: `table_name=${table_name}`,
                    headers: {
                        "Content-Type": "application/x-www-form-urlencoded",
                    },
                    method:'post',

                }).then(res => res.json()).then(data => {
                    console.log(data);
                  });
            }}>
                <ListItemIcon>
                    <AssignmentIcon />
                </ListItemIcon>
                <ListItemText primary={table_name} />
            </ListItem>
          )
        
      })

    const upload_file_from_input_event = (e) => {

      const files = e.target.files
      const formData = new FormData()
      formData.append('file', files[0])

      fetch("/upload", {
        method: "POST",
        body: formData
      }).then(res=> res.json()).then(data => {
        console.log(data);
      }).catch(error=>{
        console.error(error)
      });

    }

    const add_pcap_from_input_event = (e) => {

      const files = e.target.files
      const formData = new FormData()
      formData.append('file', files[0])

      fetch("/add_pcap", {
        method: "POST",
        body: formData
      }).then(res=> res.json()).then(data => {
        console.log(data);
      }).catch(error=>{
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
          <Divider />
          <List>{mainListItems}</List>
          <Divider />
          <ListSubheader inset>Tables</ListSubheader>
          <List>{savedTables}</List>
          <ListSubheader inset>Upload new pcap</ListSubheader>
          <Button
              variant="contained"
              component="label"
            >
              Upload File
              <input
                type="file"
                hidden
                onChange={(ev)=>{console.log("triggered onSubmit from file upload. "); console.log(ev.target); add_pcap_from_input_event(ev)}}
              />
            </Button>
        </Drawer>
    )
}



