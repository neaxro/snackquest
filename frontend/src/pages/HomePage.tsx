import InfoCard from "../components/home/InfoCard";

function HomePage() {
  return (
    <>
      <div className="container">
        <div className="text-center my-4">
          <img
            src="/SnackquestBanner.png"
            alt="Snackquest Banner"
            className="img-fluid rounded shadow-lg"
            style={{ maxHeight: "400px", objectFit: "cover" }}
          />
        </div>

        <InfoCard title="Has this ever happened to you?">
          <p>
            You wanted to clear out a vending machine, but no matter how hard
            you tried, you couldn’t zero out your balance. A few cents always
            remained stuck? Needless to say, it’s incredibly frustrating... But
            worry no more! Snackquest is here to save the day!
          </p>
        </InfoCard>

        <InfoCard title="Has this ever happened to you?">
          <p>
            <b>S</b>nacks <b>N</b>earest <b>A</b>pproach to <b>C</b>alculate{" "}
            <b>K</b>oin <b>Q</b>uota <b>U</b>tilizing<b>E</b>fficient <b>S</b>
            election <b>T</b>actics – inshort, <strong>Snackquest</strong> –is a
            program that solves an optimization problem using Linear
            Programming.
          </p>
          <p>
            It’s the ultimate solution to your vending machine challenges! Well,
            maybe not all your challenges, but it’ll definitely make clearing
            out vending machines a breeze! With Snackquest, you can efficiently
            calculate the best way to empty vending machines like a pro.
          </p>
        </InfoCard>

        <InfoCard title="How does it work?">
          <ol>
            <li>
              <strong>
                Head over to the <a href="/calculator">Calculator</a> page:
              </strong>{" "}
              Enter your current balance and copy the relevant inventory file
              from the <a href="/machines">Machines page</a>. Adjust it to suit
              your needs.
            </li>
            <li>
              <strong>Customize your preferences:</strong> The inventory file
              contains all the details, so you can specify how many items you
              want or set minimum requirements.
            </li>
            <li>
              <strong>Hit Calculate:</strong> Once you’ve set everything up,
              click the Calculate button, and in no time, Snackquest will show
              you the most optimal way to spend your money.
            </li>
          </ol>
          <p>
            Currently, the program optimizes for the maximum number of snacks.
            In the future, we plan to introduce more strategies to fit your
            preferences better.{" "}
          </p>
        </InfoCard>

        <InfoCard title="Strength in teamwork!">
          <p>
            Each vending machine’s inventory file contains all available snacks
            (with the last update date indicated in the first row), so you only
            need to use it.
            <span className="fw-bold"> You’re welcome! 😊</span>
          </p>
          <p>
            Want to help out? If you notice that a snack is out of stock, a new
            item has been added, or some prices have changed, feel free to open
            a<strong>PR (Pull Request)</strong> with the updated details in this{" "}
            <a href="https://github.com/neaxro/snackquest">repository</a>.
          </p>
        </InfoCard>
      </div>
    </>
  );
}

export default HomePage;
