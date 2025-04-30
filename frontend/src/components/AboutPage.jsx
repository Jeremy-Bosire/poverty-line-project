import '../styles/AboutPage.css'; 
function AboutPage(){
    return(
        <div className="cards">
        <div className="mission">
            <div className='titles'>
                <h1>Mission/Goal</h1>
            </div>
            <h2>Our mission at PovAware is to provide employment/income opportunities to skilled
                workers that are not able to acquire these opportunities through
                conventional means. We connect job seekers to employers who can
                select workers based on their preferred skills.
            </h2>
        </div>
        <div className='vision'>
            <div className='titles'>
                <h1>Vision</h1>
            </div>
            <h2>Our vision is to see all be able to monetise their skills and talents that are often overlooked
                during convential employment processes.
            </h2>

        </div>
        <div className='core-values'>
            <div className='titles'>
                <h1>Core Values</h1>
            </div>
            <h2>
                <ol>
                    <li>Fair opportunities for all sexes, ages and economic backgrounds.</li>
                    <li>No discrimiation based on current educational achievements.</li>
                </ol>
            </h2>

        </div>
        <div className="partner-organisations">
            <h2> (Insert Banner with  automatically scrolling images)</h2>
        </div>
        </div>
    )
}
export default AboutPage