import '../styles/OrganisationPage.css';
import React, { useState, useEffect } from 'react';
import Navbar from './Navbar';
import Select from 'react-select';


function OrganizationPage() {
  const [profiles, setProfiles] = useState([]);
  const [selectedSkills, setSelectedSkills] = useState([]);
  const [sortLocationOrder, setSortLocationOrder] = useState('asc'); 
  const [employmentStatusFilter, setEmploymentStatusFilter] = useState(''); 
  const skillOptions = [
    { value: 'writing', label: 'Writing' },
    { value: 'public_speaking', label: 'Public Speaking' },
    { value: 'coding', label: 'Coding' },
    { value: 'data_handling', label: 'Data Handling (spreadsheets)' },
    { value: 'heavy_lifting', label: 'Heavy Lifting' },
    { value: 'social_media', label: 'Social Media' },
    { value: 'vid_photo', label: 'Videography and Photography' },
    { value: 'music', label: 'Music' },
    { value: 'crafting', label: 'Craftsmanship' },
    { value: 'handiwork', label: 'Handiwork (Basic Repairs)' },
    { value: 'gardening', label: 'Gardening' },
    { value: 'cooking', label: 'Cooking' },
    { value: 'hairstyling', label: 'Hairstyling/Barbering' },
    { value: 'art_design', label: 'Art and Design' }
  ];
  


  useEffect(() => {
    // Fetch the organization data after the component mounts
    const fetchOrganizationData = async () => {
      try {
        const response = await fetch('http://localhost:5000/get_organization_data', {
          method: 'GET',
          credentials: 'include',  // Ensure cookies are sent for authentication
        });
        if (response.ok) {
            const data = await response.json();
            setProfiles(data.profiles);
          } else {
            console.error('Error: ', response.statusText);
          }
        } catch (error) {
          console.error('Error fetching organization data:', error);
        }
      };

    fetchOrganizationData();
  }, []);  

  return (
    <div>
      <Navbar/>
      <h1>Organization Dashboard</h1>
      <h2>User Profiles</h2>
      <div className="filters">
        {/* Skills Multi-Select */}
      
      <div style={{ minWidth: '250px' }}>
        <label>Skills:</label>
        <Select
          isMulti
          options={skillOptions}
          className="basic-multi-select"
          value={skillOptions.filter(option => selectedSkills.includes(option.value))}
          onChange={(selected) => {
            const values = selected.map(option => option.value);
            setSelectedSkills(values);
          }}
          placeholder="Select skills..."
        />
      </div>


        {/* Location Sort */}
        <label>
          Sort Locations:
          <select value={sortLocationOrder} onChange={(e) => setSortLocationOrder(e.target.value)}>
            <option value="asc">A-Z</option>
            <option value="desc">Z-A</option>
          </select>
        </label>

        {/* Employment Status */}
        <label>
          Employment Status:
          <select value={employmentStatusFilter} onChange={(e) => setEmploymentStatusFilter(e.target.value)}>
            <option value="">All</option>
            <option value="employed">Employed</option>
            <option value="seeking">Seeking</option>
          </select>
        </label>
      </div>

        <table>
          <thead>
            <tr>
              <th>Username</th>
              <th>Gender</th>
              <th>Location</th>
              <th>Age</th>
              <th>Skills</th>
              <th>Employment Status</th>
            </tr>
          </thead>
          <tbody>
          {profiles
            .filter(profile => {
              // Filter by employment status
              if (employmentStatusFilter && profile.employment_status !== employmentStatusFilter) {
                return false;
              }
              // Filter by selected skills
              if (selectedSkills.length > 0) {
                const userSkills = profile.skills.split(',').map(skill => skill.trim().toLowerCase());
                const matches = selectedSkills.some(skill => userSkills.includes(skill));
                if (!matches) {
                  return false;
                }
              }
              return true;
            })
            .sort((a, b) => {
              if (sortLocationOrder === 'asc') {
                return a.location.localeCompare(b.location);
              } else {
                return b.location.localeCompare(a.location);
              }
            }).map((profile, index) => (
              <tr key={index}>
                <td>{profile.username}</td>
                <td>{profile.gender}</td>
                <td>{profile.location}</td>
                <td>{profile.age}</td>
                <td>{profile.skills}</td>
                <td>{profile.employment_status}</td>
              </tr>
            ))}
          </tbody>
        </table>
        <div style={{ display: 'flex', alignItems: 'center', width: 'fit-content', margin: '0 auto' }}>
          <button className="post-jobs">
            Post Jobs
          </button>
          <button className='plus-button'>
            +
          </button>
        </div>

    </div>
  );
}

export default OrganizationPage;
