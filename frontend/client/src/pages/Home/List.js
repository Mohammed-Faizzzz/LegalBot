import React from 'react';
import './styles/List.css';

const List = ({ title, images }) => {
    return (
        <div className="list-container">
            <h1 className="list-title">{title}</h1>
            <div className="image-container">
                {images.map((image, index) => (
                    <img key={index} src={image} alt={`Image ${index}`} className="image" />
                ))}
            </div>
        </div>
    );
}

export default List;
