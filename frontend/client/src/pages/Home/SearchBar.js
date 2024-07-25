import React, { useState } from "react";
import "./styles/SearchBar.css";

const SearchBar = () => {
    const [search, setSearch] = useState("");
    
    const handleSearch = (e) => {
        setSearch(e.target.value);
    };
    
    return (
        <div>
        <input
            className="search-bar"
            type="text"
            placeholder="Search for an event"
            value={search}
            onChange={handleSearch}
        />
        </div>
    );
};

export default SearchBar;