/* reimplemented from
 * minivalidator.h
 *
 *  Created on: 24 Aug 2016
 *      Author: jkiesele
 */

#ifndef photonvalidator_H_
#define photonvalidator_H_

#include "interface/basicAnalyzer.h"
#include "interface/sampleCollection.h"
#include "classes/DelphesClasses.h"


class photonvalidator: public d_ana::basicAnalyzer{
public:
	photonvalidator():d_ana::basicAnalyzer(){}
	~photonvalidator(){}


private:
	void analyze(size_t id);

	void postProcess();
};





#endif /* photonvalidator_H_ */
