import * as React from 'react';
import PropTypes from 'prop-types';
import Typography from '@mui/material/Typography';

/**
 * A very simple functional component to render the title of the dashboard. 
 * 
 * @param {*} props 
 * @returns 
 */
function Title(props) {
  return (
    <Typography component="h2" variant="h6" color="primary" gutterBottom>
      {props.children}
    </Typography>
  );
}

Title.propTypes = {
  children: PropTypes.node,
};

export default Title;
