import * as React from 'react';
import { useState, useEffect } from 'react';
import PropTypes from 'prop-types';
import Button from '@mui/material/Button';
import Avatar from '@mui/material/Avatar';
import List from '@mui/material/List';
import ListItem from '@mui/material/ListItem';
import ListItemAvatar from '@mui/material/ListItemAvatar';
import ListItemText from '@mui/material/ListItemText';
import DialogTitle from '@mui/material/DialogTitle';
import Dialog from '@mui/material/Dialog';
import PersonIcon from '@mui/icons-material/Person';
import AddIcon from '@mui/icons-material/Add';
import Typography from '@mui/material/Typography';
import { blue } from '@mui/material/colors';
import { TextField } from '@mui/material';



function SimpleDialog(props) {
  const { onClose, newTableName, setNewTableName, open } = props;

  const handleClose = () => {
    onClose(newTableName);
  };


  return (
    <Dialog onClose={handleClose} open={open}>
      <DialogTitle>Create table</DialogTitle>
      <List sx={{ pt: 0 }}>
        <TextField id="standard-basic" defaultValue="MyNewPacketTable" onChange={e=>{setNewTableName(e.target.value)}}></TextField>
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

export default function AddTableButton(props) {
  const [open, setOpen] = useState(false);
  const [newTableName, setNewTableName] = React.useState("");

  const handleClickOpen = () => {
    setOpen(true);
  };

  const handleClose = (value) => {
    setOpen(false);
    setNewTableName(value);
    const formData = new FormData()
    formData.append('table_name', value)
    fetch("/create_table", {
      method: "POST",
      body: formData
    }).then(res=> res.json()).then(data => {
      console.log(data);
    }).catch(error=>{
      console.error(error)
    });

    console.log("Updating the dashboard from closing the SimpleDialog")
    props.setUpdateDashboard(props.updateDashboard+1);


  };

  return (
    <div>
      <Typography variant="subtitle1" component="div">
        Selected: {newTableName}
      </Typography>
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