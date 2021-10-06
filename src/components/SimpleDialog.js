import * as React from 'react';
import { useState } from 'react';
import PropTypes from 'prop-types';
import Button from '@mui/material/Button';
import Avatar from '@mui/material/Avatar';
import List from '@mui/material/List';
import ListItem from '@mui/material/ListItem';
import ListItemAvatar from '@mui/material/ListItemAvatar';
import ListItemText from '@mui/material/ListItemText';
import DialogTitle from '@mui/material/DialogTitle';
import Dialog from '@mui/material/Dialog';
import AddIcon from '@mui/icons-material/Add';
import { TextField } from '@mui/material';


/**
 * A functional component to send a simple dialog for 
 * user input
 * @param {*} props 
 * @returns 
 */
function SimpleDialog(props) {
  const { onClose, newTableName, setNewTableName, open } = props;

  const handleClose = () => {
    onClose(newTableName);
  };


  return (
    <Dialog onClose={handleClose} open={open}>
      <DialogTitle>Create table</DialogTitle>
      <List sx={{ pt: 0 }}>
        <TextField id="standard-basic" defaultValue="MyNewPacketTable" onChange={e => { setNewTableName(e.target.value) }}></TextField>
        <ListItem autoFocus button onClick={() => handleClose(newTableName)}>
          <ListItemAvatar>
            <Avatar>
              <AddIcon />
            </Avatar>
          </ListItemAvatar>
          <ListItemText primary="Add table" />
        </ListItem>
      </List>
    </Dialog>
  );
}

SimpleDialog.propTypes = {
  onClose: PropTypes.func.isRequired,
  open: PropTypes.bool.isRequired,
  newTableName: PropTypes.string.isRequired,
};


/**
 * A functional component which will create a button 
 * which will use a SimpleDialog to allow the user
 * to input the name of a new table they would like to add. 
 * 
 * @param {*} props 
 * @returns 
 */
export default function AddTableButton(props) {
  const [open, setOpen] = useState(false);
  const [newTableName, setNewTableName] = React.useState("");

  const handleClickOpen = () => {
    setOpen(true);
  };

  // when the form is submitted, send the request
  // to add the table and then refresh components. 
  const handleClose = (value) => {
    setOpen(false);
    setNewTableName(value);
    const formData = new FormData()
    formData.append('table_name', value)
    fetch("/create_table", {
      method: "POST",
      body: formData
    }).then(res => res.json()).then(data => {
      console.log(data);
    }).catch(error => {
      console.error(error)
    });

    console.log("Updating the dashboard from closing the SimpleDialog")
    props.setUpdateDashboard(props.updateDashboard + 1);


  };

  // render the button and the SimpleDialog
  return (
    <div>
      <br />
      <Button variant="contained" onClick={handleClickOpen}>
        Add Table
      </Button>
      <SimpleDialog
        newTableName={newTableName}
        setNewTableName={setNewTableName}
        open={open}
        onClose={handleClose}
      />
    </div>
  );
}