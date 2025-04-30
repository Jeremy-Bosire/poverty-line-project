import '../styles/UserForm.css';
import React, { useState} from 'react';
import Select from 'react-select';

function UserPage() {
  const [selectedSkills, setSelectedSkills] = useState([]);
  const [gender, setGender] = useState('');
  const [location, setLocation] = useState('');
  const [age, setAge] = useState(18);
  const [employmentStatus, setEmploymentStatus] = useState('');
  const [username, setUsername] = useState(null);

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

  const handleSkillChange = (selectedOptions) => {
    setSelectedSkills(selectedOptions);
  };
  const handleSubmit = async (e) => {
    e.preventDefault();
  
    const gender = document.querySelector('input[name="gender"]:checked')?.value || '';
    const location = document.getElementById('location').value;
    const age = parseInt(document.getElementById('age').value, 10);
    const employment_status = document.querySelector('input[name="employment_status"]:checked')?.value || '';
    const skills = selectedSkills.map(skill => skill.value);
    const data = { gender, location, age, skills, employment_status };
  
    try {
      const response = await fetch('http://localhost:5000/add_user', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
      });
  
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
  
      const result = await response.json();  // Only parse if response is ok
      alert('User profile submitted: ' + result.message);
  
    } catch (error) {
      console.error('Error submitting form:', error);
      alert('Error submitting form. Check console.');
    }
  };
 
  

  return (
    <div>
      <h1>Welcome to PovAware!</h1>
      <h1>Add your details</h1>
      <form className="user-form-container" onSubmit={handleSubmit}>
        {/* Gender */}
        <label>Gender:</label><br />
        <input
          type="radio"
          id="male"
          name="gender"
          value="male"
          onChange={(e) => setGender(e.target.value)}
        />
        <label htmlFor="male">Male</label>
        <input
          type="radio"
          id="female"
          name="gender"
          value="female"
          onChange={(e) => setGender(e.target.value)}
        />
        <label htmlFor="female">Female</label>
        <br /><br />

        {/* Location */}
        <label htmlFor="location">Location:</label><br />
        <input
          type="text"
          id="location"
          name="location"
          value={location}
          onChange={(e) => setLocation(e.target.value)}
        />
        <br /><br />

        {/* Age */}
        <label htmlFor="age">Age:</label><br />
        <input
          type="number"
          id="age"
          name="age"
          value={age}
          onChange={(e) => setAge(Number(e.target.value))}
        />
        <br /><br />

        {/* Skills */}
        <label htmlFor="skills">Skills:</label><br />
        <Select
          isMulti
          name="skills"
          options={skillOptions}
          className="basic-multi-select"
          classNamePrefix="select"
          onChange={handleSkillChange}
          value={selectedSkills}
        />
        <br /><br />

        {/* Employment Status */}
        <label>Employment Status:</label><br />
        <input
          type="radio"
          id="employed"
          name="employment_status"
          value="employed"
          onChange={(e) => setEmploymentStatus(e.target.value)}
        />
        <label htmlFor="employed">Employed</label>
        <input
          type="radio"
          id="seeking"
          name="employment_status"
          value="seeking"
          onChange={(e) => setEmploymentStatus(e.target.value)}
        />
        <label htmlFor="seeking">Seeking</label>
        <br /><br />

        {/* Submit Button */}
        <button type="submit">Submit</button>
      </form>

      <form className="feedback-form-container">
        <label htmlFor="areaUpdate">What's happening in your area?</label>
        <input type="text" id="areaUpdate" name="areaUpdate" placeholder="Let us know" />
      </form>
    </div>
  );
}

export default UserPage;
