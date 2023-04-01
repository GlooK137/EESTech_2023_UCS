import React from 'react';
import { Button, Icon } from 'react-native-elements';

const IconButton = ({ icon, onPress }) => {
  return (
    <Button
    type='cleat'
      icon={
        <Icon
          name={icon}
          size={24}
          color="white"
        />
      }
      onPress={onPress}
    />
  );
};

export default IconButton;
