import './App.css';
import React, { useState } from 'react';
import axios from 'axios';

const App = () => {
  const [keyword, setKeyword] = useState('');
  const [salaryFilter, setSalaryFilter] = useState('');
  const [requirementFilter, setRequirementFilter] = useState('');
  const [vacancies, setVacancies] = useState([]);

  const search = async () => {
    try {
      const response = await axios.post('http://localhost:8000/vacancies', { keyword });
      setVacancies(response.data);
    } catch (error) {
      console.error(error);
    }
  };

  const filterVacancies = () => {
    let filteredVacancies = vacancies;

    if (salaryFilter) {
      filteredVacancies = filteredVacancies.filter(vacancy => {
        if (vacancy.salary) {
          return vacancy.salary.from >= salaryFilter;
        }
        return false;
      });
    }

    if (requirementFilter) {
      filteredVacancies = filteredVacancies.filter(vacancy => vacancy.snippet.requirement.toLowerCase().includes(requirementFilter.toLowerCase()));
    }

    return filteredVacancies;
  };

  const handleSalaryFilterChange = (e) => {
    setSalaryFilter(e.target.value);
  };

  const handleRequirementFilterChange = (e) => {
    setRequirementFilter(e.target.value);
  };

  return (
    <div className='app'>
      <div className='search'>
        <input
          className='input'
          type='text'
          value={keyword}
          onChange={(e) => setKeyword(e.target.value)}
          placeholder='Введите ваш запрос...'
        />
        <button className='search_button' onClick={search}>Поиск</button>
      </div>
      <div className='filters'>
        <h3>Фильтры:</h3>
        <label>Минимальная зарплата:
          <input type='number' value={salaryFilter} onChange={handleSalaryFilterChange} />
        </label>
        <br />
        <label>Требования:
          <input type='text' value={requirementFilter} onChange={handleRequirementFilterChange} />
        </label>
      </div>
      <div className='vacancy_list'>
        <ol>
          {filterVacancies().map(vacancy => (
            <li key={vacancy.id}>
              <h3>{vacancy.name}</h3>
              <p>Компания: {vacancy.employer.name}</p>
              <p>Регион: {vacancy.area.name}</p>
              <p>Зарплата: {vacancy.salary ? `${vacancy.salary.from} - ${vacancy.salary.to} ${vacancy.salary.currency}` : 'Не указано'}</p>
              <p>Требования: {vacancy.snippet.requirement ? vacancy.snippet.requirement : 'Не указано'}</p>
              <a href={vacancy.alternate_url} target="_blank" rel="noopener noreferrer">Просмотреть вакансию</a>
            </li>
          ))}
        </ol>
      </div>
    </div>
  );
};

export default App;