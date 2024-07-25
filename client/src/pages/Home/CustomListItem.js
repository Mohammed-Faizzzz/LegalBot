import React from 'react';
import ListItem from '@mui/material/ListItem';
import ListItemButton from '@mui/material/ListItemButton';
import ListItemIcon from '@mui/material/ListItemIcon';
import ListItemText from '@mui/material/ListItemText';
import Collapse from '@mui/material/Collapse';
import './styles/CustomListItem.css';

const CustomListItem = ({
  IconComponent,
  primary,
  onClick,
  expandable = false,
  isOpen = false,
  children,
  collapseStyle = {}
}) => {
  return (
    <>
      <ListItem onClick={onClick} className="custom-list-item">
        <ListItemButton>
          {/* <ListItemIcon className="list-item-icon">
            <IconComponent/>
          </ListItemIcon> */}
          <ListItemText primary={primary} />
        </ListItemButton>
      </ListItem>
      {expandable && (
        <Collapse in={isOpen} style={collapseStyle}>
          {children}
        </Collapse>
      )}
    </>
  );
};

export default CustomListItem;
